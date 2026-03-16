from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.books.service import BookService

async def get_book_service(db: Session = Depends(get_db)):
    return BookService(db)