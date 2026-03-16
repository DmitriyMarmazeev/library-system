from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import Optional, List
from datetime import date, timedelta

from app.modules.loans.models import Loan, LoanStatus
from app.modules.copies.models import Copy, CopyStatus
from app.modules.users.models import User
from app.modules.books.models import Book

class LoanRepository:
    def __init__(self, db: Session):
        self.db = db
    
    # Basic CRUD
    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        return self.db.query(Loan).filter(Loan.id == loan_id).first()
    
    def get_by_id_with_details(self, loan_id: int) -> Optional[Loan]:
        return self.db.query(Loan)\
            .options(
                joinedload(Loan.copy).joinedload(Copy.book),
                joinedload(Loan.user)
            )\
            .filter(Loan.id == loan_id)\
            .first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        return self.db.query(Loan)\
            .order_by(Loan.loan_date.desc())\
            .offset(skip).limit(limit)\
            .all()
    
    def create(self, loan_data: dict) -> Loan:
        loan = Loan(**loan_data)
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan
    
    def update(self, loan_id: int, loan_data: dict) -> Optional[Loan]:
        loan = self.get_by_id(loan_id)
        if loan:
            for key, value in loan_data.items():
                if value is not None:
                    setattr(loan, key, value)
            self.db.commit()
            self.db.refresh(loan)
        return loan
    
    # Active loans
    def get_active_loans(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        return self.db.query(Loan)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .order_by(Loan.due_date)\
            .offset(skip).limit(limit)\
            .all()
    
    def get_active_loans_with_details(self, skip: int = 0, limit: int = 100) -> List[Loan]:
        return self.db.query(Loan)\
            .options(
                joinedload(Loan.copy).joinedload(Copy.book),
                joinedload(Loan.user)
            )\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .order_by(Loan.due_date)\
            .offset(skip).limit(limit)\
            .all()
    
    def get_active_loan_by_copy(self, copy_id: int) -> Optional[Loan]:
        return self.db.query(Loan)\
            .filter(Loan.copy_id == copy_id)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .first()
    
    def get_active_loans_by_user(self, user_id: int) -> List[Loan]:
        return self.db.query(Loan)\
            .options(joinedload(Loan.copy).joinedload(Copy.book))\
            .filter(Loan.user_id == user_id)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .all()
    
    # Overdue loans
    def get_overdue_loans(self) -> List[Loan]:
        today = date.today()
        return self.db.query(Loan)\
            .options(
                joinedload(Loan.copy).joinedload(Copy.book),
                joinedload(Loan.user)
            )\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .filter(Loan.due_date < today)\
            .order_by(Loan.due_date)\
            .all()
    
    def update_overdue_status(self):
        """Update status of loans that are overdue"""
        today = date.today()
        overdue_loans = self.db.query(Loan)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .filter(Loan.due_date < today)\
            .all()
        
        for loan in overdue_loans:
            loan.status = LoanStatus.OVERDUE
        
        self.db.commit()
        return len(overdue_loans)
    
    # User history
    def get_user_loan_history(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        return self.db.query(Loan)\
            .options(joinedload(Loan.copy).joinedload(Copy.book))\
            .filter(Loan.user_id == user_id)\
            .order_by(Loan.loan_date.desc())\
            .offset(skip).limit(limit)\
            .all()
    
    def get_user_active_loans_count(self, user_id: int) -> int:
        return self.db.query(Loan)\
            .filter(Loan.user_id == user_id)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .count()
    
    def get_user_overdue_loans_count(self, user_id: int) -> int:
        today = date.today()
        return self.db.query(Loan)\
            .filter(Loan.user_id == user_id)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .filter(Loan.due_date < today)\
            .count()
    
    # Copy history
    def get_copy_loan_history(self, copy_id: int) -> List[Loan]:
        return self.db.query(Loan)\
            .filter(Loan.copy_id == copy_id)\
            .order_by(Loan.loan_date.desc())\
            .all()
    
    # Returns
    def return_loan(self, loan_id: int, return_date: Optional[date] = None) -> Optional[Loan]:
        loan = self.get_by_id(loan_id)
        if loan and loan.status in [LoanStatus.ACTIVE, LoanStatus.OVERDUE]:
            loan.return_date = return_date or date.today()
            loan.status = LoanStatus.RETURNED
            self.db.commit()
            self.db.refresh(loan)
        return loan
    
    # Statistics
    def get_active_loans_count(self) -> int:
        return self.db.query(Loan)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .count()
    
    def get_overdue_loans_count(self) -> int:
        today = date.today()
        return self.db.query(Loan)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .filter(Loan.due_date < today)\
            .count()
    
    def get_today_returns_count(self) -> int:
        today = date.today()
        return self.db.query(Loan)\
            .filter(Loan.return_date == today)\
            .count()
    
    def get_today_loans_count(self) -> int:
        today = date.today()
        return self.db.query(Loan)\
            .filter(Loan.loan_date == today)\
            .count()
    
    def get_average_loan_duration(self) -> Optional[float]:
        result = self.db.query(
            func.avg(Loan.return_date - Loan.loan_date)
        ).filter(Loan.return_date.isnot(None)).scalar()
        
        if result:
            return float(result.days) if hasattr(result, 'days') else float(result)
        return None
    
    def get_most_active_users(self, limit: int = 5) -> List[dict]:
        result = self.db.query(
            User.id,
            User.first_name,
            User.last_name,
            func.count(Loan.id).label('loan_count')
        ).join(Loan, Loan.user_id == User.id)\
         .group_by(User.id)\
         .order_by(func.count(Loan.id).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                "user_id": r[0],
                "user_name": f"{r[1]} {r[2]}",
                "loan_count": r[3]
            }
            for r in result
        ]
    
    def get_most_borrowed_books(self, limit: int = 5) -> List[dict]:
        result = self.db.query(
            Book.id,
            Book.title,
            func.count(Loan.id).label('loan_count')
        ).join(Copy, Copy.book_id == Book.id)\
         .join(Loan, Loan.copy_id == Copy.id)\
         .group_by(Book.id)\
         .order_by(func.count(Loan.id).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                "book_id": r[0],
                "book_title": r[1],
                "loan_count": r[2]
            }
            for r in result
        ]