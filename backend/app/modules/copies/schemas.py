from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CopyStatusEnum(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    DAMAGED = "damaged"
    LOST = "lost"

class CopyBase(BaseModel):
    book_id: int
    location: Optional[str] = Field(None, max_length=100)

class CopyCreate(CopyBase):
    pass

class CopyUpdate(BaseModel):
    status: Optional[CopyStatusEnum] = None
    location: Optional[str] = Field(None, max_length=100)

class CopyResponse(CopyBase):
    id: int
    status: CopyStatusEnum
    
    class Config:
        from_attributes = True

class CopyDetailResponse(CopyResponse):
    book_title: str
    book_isbn: Optional[str] = None
    current_loan_id: Optional[int] = None
    loan_history_count: int = 0
    
    class Config:
        from_attributes = True

class CopyStatusUpdate(BaseModel):
    status: CopyStatusEnum
    reason: Optional[str] = Field(None, max_length=255)

class CopyBulkCreate(BaseModel):
    book_id: int
    count: int = Field(1, ge=1, le=100)
    location: Optional[str] = None

class CopyBulkCreateResponse(BaseModel):
    book_id: int
    book_title: str
    created_count: int
    copy_ids: List[int]

class CopyLoanHistory(BaseModel):
    loan_id: int
    reader_name: str
    loan_date: datetime
    return_date: Optional[datetime]
    status: str
    
    class Config:
        from_attributes = True