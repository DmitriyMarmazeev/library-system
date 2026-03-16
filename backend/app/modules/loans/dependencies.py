from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.loans.service import LoanService

async def get_loan_service(db: Session = Depends(get_db)):
    return LoanService(db)