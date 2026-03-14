from sqlalchemy import Column, Integer, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class LoanStatus(str, enum.Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

class Loan(Base):
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True, index=True)
    copy_id = Column(Integer, ForeignKey('copies.id', ondelete='RESTRICT'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    loan_date = Column(Date, nullable=False, server_default=func.current_date())
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE, nullable=False)
    
    # Relationships
    copy = relationship("Copy", back_populates="loans")
    user = relationship("User", back_populates="loans")