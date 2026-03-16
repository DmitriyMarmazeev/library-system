from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.copies.service import CopyService

async def get_copy_service(db: Session = Depends(get_db)):
    return CopyService(db)