from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.modules.copies.repository import CopyRepository
from app.modules.copies.schemas import CopyCreate, CopyUpdate, CopyStatusUpdate, CopyBulkCreate
from app.modules.copies.models import CopyStatus
from app.modules.books.repository import BookRepository
from app.modules.loans.repository import LoanRepository

class CopyService:
    def __init__(self, db: Session):
        self.db = db
        self.copy_repo = CopyRepository(db)
        self.book_repo = BookRepository(db)
        self.loan_repo = LoanRepository(db)
    
    def get_copy_by_id(self, copy_id: int):
        copy = self.copy_repo.get_by_id_with_details(copy_id)
        if not copy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Copy not found"
            )
        return copy
    
    def get_all_copies(self, skip: int = 0, limit: int = 100):
        copies = self.copy_repo.get_all_with_details(skip, limit)
        return copies
    
    def get_copies_by_book(self, book_id: int, skip: int = 0, limit: int = 100):
        # Check if book exists
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        return self.copy_repo.get_by_book_id(book_id, skip, limit)
    
    def create_copy(self, copy_data: CopyCreate):
        # Check if book exists
        book = self.book_repo.get_by_id(copy_data.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        copy = self.copy_repo.create(copy_data.dict())
        return copy
    
    def create_copies_bulk(self, bulk_data: CopyBulkCreate):
        # Check if book exists
        book = self.book_repo.get_by_id(bulk_data.book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        copies = self.copy_repo.create_multiple(
            book_id=bulk_data.book_id,
            count=bulk_data.count,
            location=bulk_data.location
        )
        
        return {
            "book_id": book.id,
            "book_title": book.title,
            "created_count": len(copies),
            "copy_ids": [c.id for c in copies]
        }
    
    def update_copy(self, copy_id: int, copy_data: CopyUpdate):
        copy = self.get_copy_by_id(copy_id)
        
        # Special validation for status changes
        if copy_data.status:
            self._validate_status_change(copy, copy_data.status)
        
        update_dict = copy_data.dict(exclude_unset=True)
        updated_copy = self.copy_repo.update(copy_id, update_dict)
        
        return updated_copy
    
    def update_copy_status(self, copy_id: int, status_update: CopyStatusUpdate):
        copy = self.get_copy_by_id(copy_id)
        
        # Validate status change
        self._validate_status_change(copy, status_update.status)
        
        updated_copy = self.copy_repo.update_status(copy_id, status_update.status)
        
        # Log status change (can be extended with a status history table)
        
        return updated_copy
    
    def delete_copy(self, copy_id: int):
        copy = self.get_copy_by_id(copy_id)
        
        # Check if copy has any loan history
        if copy.loans:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete copy with loan history"
            )
        
        deleted = self.copy_repo.delete(copy_id)
        return {"message": "Copy deleted successfully"}
    
    def get_copy_details(self, copy_id: int):
        copy = self.get_copy_by_id(copy_id)
        
        # Get current loan if any
        current_loan = self.copy_repo.get_current_loan(copy_id)
        
        # Get loan history count
        loan_history = self.copy_repo.get_loan_history(copy_id, limit=1)
        history_count = len(copy.loans) if copy.loans else 0
        
        # Create detailed response
        detail = {
            "id": copy.id,
            "book_id": copy.book_id,
            "book_title": copy.book.title if copy.book else "Unknown",
            "book_isbn": copy.book.isbn if copy.book else None,
            "status": copy.status,
            "location": copy.location,
            "current_loan_id": current_loan.id if current_loan else None,
            "loan_history_count": history_count
        }
        
        return detail
    
    def get_copy_loan_history(self, copy_id: int, skip: int = 0, limit: int = 100):
        copy = self.get_copy_by_id(copy_id)
        
        loans = self.copy_repo.get_loan_history(copy_id, skip, limit)
        
        history = []
        for loan in loans:
            history.append({
                "loan_id": loan.id,
                "reader_name": f"{loan.user.last_name} {loan.user.first_name}" if loan.user else "Unknown",
                "loan_date": loan.loan_date,
                "return_date": loan.return_date,
                "status": loan.status
            })
        
        return history
    
    def get_copies_by_status(self, status: CopyStatus, skip: int = 0, limit: int = 100):
        return self.copy_repo.get_copies_by_status(status, skip, limit)
    
    def get_book_copies_summary(self, book_id: int):
        # Check if book exists
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        total = self.copy_repo.get_by_book_id(book_id, limit=1000)
        
        return {
            "book_id": book_id,
            "book_title": book.title,
            "total_copies": len(total),
            "available": self.copy_repo.get_available_count(book_id),
            "borrowed": self.copy_repo.get_borrowed_count(book_id),
            "damaged": self.copy_repo.get_damaged_count(book_id),
            "lost": self.copy_repo.get_lost_count(book_id)
        }
    
    def search_by_location(self, location: str):
        return self.copy_repo.search_by_location(location)
    
    def _validate_status_change(self, copy, new_status: CopyStatus):
        """Validate if status change is allowed"""
        # Cannot change from certain statuses without proper actions
        if copy.status == CopyStatus.LOST and new_status != CopyStatus.LOST:
            # Found a lost copy - should be handled by librarian
            pass
        
        if copy.status == CopyStatus.BORROWED and new_status != CopyStatus.BORROWED:
            # Check if copy is actually returned
            current_loan = self.copy_repo.get_current_loan(copy.id)
            if current_loan and new_status != CopyStatus.AVAILABLE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot change status of borrowed copy. Return it first."
                )
        
        if copy.status == CopyStatus.DAMAGED and new_status == CopyStatus.AVAILABLE:
            # Damaged copy can be made available after repair
            pass
        
        return True