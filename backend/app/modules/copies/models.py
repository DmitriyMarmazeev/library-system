from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class CopyStatus(str, enum.Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    DAMAGED = "damaged"
    LOST = "lost"

class Copy(Base):
    __tablename__ = 'copies'
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    status = Column(Enum(CopyStatus), default=CopyStatus.AVAILABLE, nullable=False)
    location = Column(String(100), nullable=True)
    
    # Relationships
    book = relationship("Book", back_populates="copies")
    loans = relationship("Loan", back_populates="copy")