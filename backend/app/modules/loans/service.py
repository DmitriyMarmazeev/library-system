from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date, timedelta

from app.modules.loans.repository import LoanRepository
from app.modules.loans.schemas import LoanCreate, LoanReturn, LoanExtend, LoanStatusEnum
from app.modules.loans.models import LoanStatus
from app.modules.copies.repository import CopyRepository
from app.modules.copies.models import CopyStatus
from app.modules.users.repository import UserRepository
from app.modules.books.repository import BookRepository

class LoanService:
    def __init__(self, db: Session):
        self.db = db
        self.loan_repo = LoanRepository(db)
        self.copy_repo = CopyRepository(db)
        self.user_repo = UserRepository(db)
        self.book_repo = BookRepository(db)
    
    def get_loan_by_id(self, loan_id: int):
        loan = self.loan_repo.get_by_id_with_details(loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Loan not found"
            )
        
        # Calculate days overdue/remaining
        days_overdue = 0
        days_remaining = 0
        today = date.today()
        
        if loan.return_date:
            # Returned loan
            pass
        elif loan.due_date < today:
            days_overdue = (today - loan.due_date).days
        else:
            days_remaining = (loan.due_date - today).days
        
        # Construct detailed response
        return {
            "id": loan.id,
            "copy_id": loan.copy_id,
            "user_id": loan.user_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "status": loan.status,
            "book_title": loan.copy.book.title if loan.copy and loan.copy.book else "Unknown",
            "book_isbn": loan.copy.book.isbn if loan.copy and loan.copy.book else None,
            "copy_location": loan.copy.location if loan.copy else None,
            "user_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
            "user_email": loan.user.email if loan.user else "Unknown",
            "days_overdue": days_overdue,
            "days_remaining": days_remaining
        }
    
    def get_all_loans(self, skip: int = 0, limit: int = 100):
        loans = self.loan_repo.get_all(skip, limit)
        
        result = []
        for loan in loans:
            # Загружаем связанные данные для каждого loan
            loan_with_details = self.loan_repo.get_by_id_with_details(loan.id)
            if loan_with_details:
                # Calculate days overdue/remaining
                days_overdue = 0
                days_remaining = 0
                today = date.today()
                
                if loan_with_details.return_date:
                    # Returned loan
                    pass
                elif loan_with_details.due_date < today:
                    days_overdue = (today - loan_with_details.due_date).days
                else:
                    days_remaining = (loan_with_details.due_date - today).days
                
                result.append({
                    "id": loan_with_details.id,
                    "copy_id": loan_with_details.copy_id,
                    "user_id": loan_with_details.user_id,
                    "loan_date": loan_with_details.loan_date,
                    "due_date": loan_with_details.due_date,
                    "return_date": loan_with_details.return_date,
                    "status": loan_with_details.status,
                    "book_title": loan_with_details.copy.book.title if loan_with_details.copy and loan_with_details.copy.book else "Unknown",
                    "book_isbn": loan_with_details.copy.book.isbn if loan_with_details.copy and loan_with_details.copy.book else None,
                    "copy_location": loan_with_details.copy.location if loan_with_details.copy else None,
                    "user_name": f"{loan_with_details.user.last_name} {loan_with_details.user.first_name}" if loan_with_details.user else "Unknown",
                    "user_email": loan_with_details.user.email if loan_with_details.user else "Unknown",
                    "days_overdue": days_overdue,
                    "days_remaining": days_remaining
                })
        
        return result
    
    def create_loan(self, loan_data: LoanCreate):
        # Check if copy exists
        copy = self.copy_repo.get_by_id(loan_data.copy_id)
        if not copy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Copy not found"
            )
        
        # Check if copy is available
        if copy.status != CopyStatus.AVAILABLE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Copy is not available (status: {copy.status})"
            )
        
        # Check if user exists
        user = self.user_repo.get_by_id(loan_data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Check if user has any overdue loans
        overdue_count = self.loan_repo.get_user_overdue_loans_count(loan_data.user_id)
        if overdue_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has overdue loans. Cannot borrow more books."
            )
        
        # Check if user has reached maximum loans (optional, e.g., 5 books at once)
        active_count = self.loan_repo.get_user_active_loans_count(loan_data.user_id)
        if active_count >= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User has reached maximum number of active loans (5)"
            )
        
        # Create loan
        loan_dict = loan_data.dict()
        loan_dict['loan_date'] = date.today()
        loan_dict['status'] = LoanStatus.ACTIVE
        
        loan = self.loan_repo.create(loan_dict)
        
        # Update copy status
        self.copy_repo.update_status(loan_data.copy_id, CopyStatus.BORROWED)
        
        return loan
    
    def return_loan(self, loan_id: int, return_data: Optional[LoanReturn] = None):
        loan = self.loan_repo.get_by_id_with_details(loan_id)
        
        # Check if loan is already returned
        if loan.status == LoanStatus.RETURNED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Loan is already returned"
            )
        
        return_date = return_data.return_date if return_data else date.today()
        
        # Process return
        returned_loan = self.loan_repo.return_loan(loan_id, return_date)
        
        # Update copy status back to available
        if returned_loan:
            self.copy_repo.update_status(loan.copy_id, CopyStatus.AVAILABLE)
        
        return returned_loan
    
    def extend_loan(self, loan_id: int, extend_data: LoanExtend):
        loan = self.loan_repo.get_by_id_with_details(loan_id)
        
        # Check if loan is active
        if loan.status not in [LoanStatus.ACTIVE, LoanStatus.OVERDUE]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only extend active or overdue loans"
            )
        
        # Check if new due date is reasonable (e.g., max 30 days extension)
        max_due_date = date.today() + timedelta(days=30)
        if extend_data.new_due_date > max_due_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Extension cannot exceed {max_due_date}"
            )
        
        # Update due date
        loan.due_date = extend_data.new_due_date
        
        # If loan was overdue, set it back to active
        if loan.status == LoanStatus.OVERDUE:
            loan.status = LoanStatus.ACTIVE
        
        self.db.commit()
        self.db.refresh(loan)
        
        return loan
    
    def get_active_loans(self, skip: int = 0, limit: int = 100):
        # Update overdue status first
        self.loan_repo.update_overdue_status()
        
        loans = self.loan_repo.get_active_loans_with_details(skip, limit)
        
        result = []
        for loan in loans:
            days_remaining = (loan.due_date - date.today()).days
            result.append({
                "id": loan.id,
                "copy_id": loan.copy_id,
                "book_title": loan.copy.book.title if loan.copy and loan.copy.book else "Unknown",
                "user_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
                "loan_date": loan.loan_date,
                "due_date": loan.due_date,
                "days_remaining": days_remaining,
                "is_overdue": days_remaining < 0
            })
        
        return result
    
    def get_overdue_loans(self):
        loans = self.loan_repo.get_overdue_loans()
        
        result = []
        for loan in loans:
            days_overdue = (date.today() - loan.due_date).days
            result.append({
                "id": loan.id,
                "copy_id": loan.copy_id,
                "book_title": loan.copy.book.title if loan.copy and loan.copy.book else "Unknown",
                "user_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
                "user_email": loan.user.email if loan.user else "Unknown",
                "user_phone": loan.user.phone if loan.user else None,
                "loan_date": loan.loan_date,
                "due_date": loan.due_date,
                "days_overdue": days_overdue
            })
        
        return result
    
    def get_user_loans(self, user_id: int, skip: int = 0, limit: int = 100):
        # Check if user exists
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        loans = self.loan_repo.get_user_loan_history(user_id, skip, limit)
        
        result = []
        for loan in loans:
            result.append({
                "id": loan.id,
                "book_title": loan.copy.book.title if loan.copy and loan.copy.book else "Unknown",
                "book_isbn": loan.copy.book.isbn if loan.copy and loan.copy.book else None,
                "loan_date": loan.loan_date,
                "due_date": loan.due_date,
                "return_date": loan.return_date,
                "status": loan.status
            })
        
        return result
    
    def get_user_active_loans(self, user_id: int):
        # Check if user exists
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        loans = self.loan_repo.get_active_loans_by_user(user_id)
        
        result = []
        for loan in loans:
            days_remaining = (loan.due_date - date.today()).days
            result.append({
                "id": loan.id,
                "copy_id": loan.copy_id,
                "book_title": loan.copy.book.title if loan.copy and loan.copy.book else "Unknown",
                "user_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
                "loan_date": loan.loan_date,
                "due_date": loan.due_date,
                "days_remaining": days_remaining,
                "is_overdue": days_remaining < 0
            })
        
        return result
    
    def get_copy_loan_history(self, copy_id: int):
        # Check if copy exists
        copy = self.copy_repo.get_by_id(copy_id)
        if not copy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Copy not found"
            )
        
        loans = self.loan_repo.get_copy_loan_history(copy_id)
        
        result = []
        for loan in loans:
            result.append({
                "loan_id": loan.id,
                "user_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
                "loan_date": loan.loan_date,
                "return_date": loan.return_date,
                "status": loan.status
            })
        
        return result
    
    def get_loan_statistics(self):
        # Update overdue status first
        self.loan_repo.update_overdue_status()
        
        stats = {
            "total_active": self.loan_repo.get_active_loans_count(),
            "total_overdue": self.loan_repo.get_overdue_loans_count(),
            "total_returned_today": self.loan_repo.get_today_returns_count(),
            "total_loans_today": self.loan_repo.get_today_loans_count(),
            "average_loan_duration": self.loan_repo.get_average_loan_duration(),
            "most_active_users": self.loan_repo.get_most_active_users(),
            "most_borrowed_books": self.loan_repo.get_most_borrowed_books()
        }
        
        return stats
    
    def check_user_can_borrow(self, user_id: int) -> dict:
        """Check if user is eligible to borrow more books"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        active_count = self.loan_repo.get_user_active_loans_count(user_id)
        overdue_count = self.loan_repo.get_user_overdue_loans_count(user_id)
        
        return {
            "user_id": user_id,
            "user_name": f"{user.last_name} {user.first_name}",
            "can_borrow": active_count < 5 and overdue_count == 0,
            "active_loans": active_count,
            "overdue_loans": overdue_count,
            "max_loans": 5
        }
    
    def process_daily_overdue(self) -> dict:
        """Daily job to process overdue loans"""
        updated_count = self.loan_repo.update_overdue_status()
        
        # Get all overdue loans for notifications
        overdue_loans = self.loan_repo.get_overdue_loans()
        
        return {
            "processed_count": updated_count,
            "total_overdue": len(overdue_loans),
            "date": date.today().isoformat()
        }