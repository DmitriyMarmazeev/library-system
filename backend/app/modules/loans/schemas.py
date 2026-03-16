from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class LoanStatusEnum(str, Enum):
    ACTIVE = "active"
    RETURNED = "returned"
    OVERDUE = "overdue"

class LoanBase(BaseModel):
    copy_id: int
    user_id: int
    due_date: date

class LoanCreate(LoanBase):
    @validator('due_date')
    def validate_due_date(cls, v):
        if v < date.today():
            raise ValueError('Due date cannot be in the past')
        return v

class LoanReturn(BaseModel):
    return_date: Optional[date] = None
    
    @validator('return_date')
    def validate_return_date(cls, v):
        if v and v > date.today():
            raise ValueError('Return date cannot be in the future')
        return v

class LoanExtend(BaseModel):
    new_due_date: date
    reason: Optional[str] = Field(None, max_length=255)
    
    @validator('new_due_date')
    def validate_new_due_date(cls, v):
        if v <= date.today():
            raise ValueError('New due date must be in the future')
        return v

class LoanResponse(BaseModel):
    id: int
    copy_id: int
    user_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date]
    status: LoanStatusEnum
    
    class Config:
        from_attributes = True

class LoanDetailResponse(LoanResponse):
    book_title: str
    book_isbn: Optional[str]
    copy_location: Optional[str]
    user_name: str
    user_email: str
    days_overdue: Optional[int] = 0
    days_remaining: Optional[int] = 0
    
    class Config:
        from_attributes = True

class ActiveLoanResponse(BaseModel):
    id: int
    copy_id: int
    book_title: str
    user_name: str
    loan_date: date
    due_date: date
    days_remaining: int
    is_overdue: bool
    
    class Config:
        from_attributes = True

class UserLoanHistory(BaseModel):
    id: int
    book_title: str
    book_isbn: Optional[str]
    loan_date: date
    due_date: date
    return_date: Optional[date]
    status: LoanStatusEnum
    
    class Config:
        from_attributes = True

class OverdueLoanResponse(BaseModel):
    id: int
    copy_id: int
    book_title: str
    user_name: str
    user_email: str
    user_phone: Optional[str]
    loan_date: date
    due_date: date
    days_overdue: int
    
    class Config:
        from_attributes = True

class LoanStatsResponse(BaseModel):
    total_active: int
    total_overdue: int
    total_returned_today: int
    total_loans_today: int
    average_loan_duration: Optional[float]
    most_active_users: List[dict]
    most_borrowed_books: List[dict]