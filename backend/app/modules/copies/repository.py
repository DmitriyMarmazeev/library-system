from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import Optional, List
from app.modules.copies.models import Copy, CopyStatus
from app.modules.books.models import Book
from app.modules.loans.models import Loan, LoanStatus

class CopyRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, copy_id: int) -> Optional[Copy]:
        return self.db.query(Copy).filter(Copy.id == copy_id).first()
    
    def get_by_id_with_details(self, copy_id: int) -> Optional[Copy]:
        return self.db.query(Copy)\
            .options(joinedload(Copy.book), joinedload(Copy.loans))\
            .filter(Copy.id == copy_id)\
            .first()
    
    def get_by_book_id(self, book_id: int, skip: int = 0, limit: int = 100) -> List[Copy]:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .offset(skip).limit(limit)\
            .all()
    
    def get_available_by_book_id(self, book_id: int) -> List[Copy]:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.AVAILABLE)\
            .all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Copy]:
        return self.db.query(Copy).offset(skip).limit(limit).all()
    
    def get_all_with_details(self, skip: int = 0, limit: int = 100) -> List[Copy]:
        return self.db.query(Copy)\
            .options(joinedload(Copy.book))\
            .offset(skip).limit(limit)\
            .all()
    
    def create(self, copy_data: dict) -> Copy:
        copy = Copy(**copy_data)
        self.db.add(copy)
        self.db.commit()
        self.db.refresh(copy)
        return copy
    
    def create_multiple(self, book_id: int, count: int, location: Optional[str] = None) -> List[Copy]:
        copies = []
        for i in range(count):
            copy = Copy(
                book_id=book_id,
                status=CopyStatus.AVAILABLE,
                location=location
            )
            self.db.add(copy)
            copies.append(copy)
        
        self.db.commit()
        
        # Refresh all copies
        for copy in copies:
            self.db.refresh(copy)
        
        return copies
    
    def update(self, copy_id: int, copy_data: dict) -> Optional[Copy]:
        copy = self.get_by_id(copy_id)
        if copy:
            for key, value in copy_data.items():
                if value is not None:
                    setattr(copy, key, value)
            self.db.commit()
            self.db.refresh(copy)
        return copy
    
    def update_status(self, copy_id: int, status: CopyStatus) -> Optional[Copy]:
        copy = self.get_by_id(copy_id)
        if copy:
            copy.status = status
            self.db.commit()
            self.db.refresh(copy)
        return copy
    
    def delete(self, copy_id: int) -> bool:
        copy = self.get_by_id(copy_id)
        if copy:
            self.db.delete(copy)
            self.db.commit()
            return True
        return False
    
    def get_available_count(self, book_id: int) -> int:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.AVAILABLE)\
            .count()
    
    def get_borrowed_count(self, book_id: int) -> int:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.BORROWED)\
            .count()
    
    def get_damaged_count(self, book_id: int) -> int:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.DAMAGED)\
            .count()
    
    def get_lost_count(self, book_id: int) -> int:
        return self.db.query(Copy)\
            .filter(Copy.book_id == book_id)\
            .filter(Copy.status == CopyStatus.LOST)\
            .count()
    
    def get_current_loan(self, copy_id: int) -> Optional[Loan]:
        return self.db.query(Loan)\
            .filter(Loan.copy_id == copy_id)\
            .filter(Loan.status == LoanStatus.ACTIVE)\
            .first()
    
    def get_loan_history(self, copy_id: int, skip: int = 0, limit: int = 100) -> List[Loan]:
        return self.db.query(Loan)\
            .filter(Loan.copy_id == copy_id)\
            .order_by(Loan.loan_date.desc())\
            .offset(skip).limit(limit)\
            .all()
    
    def get_copies_by_status(self, status: CopyStatus, skip: int = 0, limit: int = 100) -> List[Copy]:
        return self.db.query(Copy)\
            .filter(Copy.status == status)\
            .offset(skip).limit(limit)\
            .all()
    
    def search_by_location(self, location: str) -> List[Copy]:
        search_term = f"%{location}%"
        return self.db.query(Copy)\
            .filter(Copy.location.ilike(search_term))\
            .limit(20).all()