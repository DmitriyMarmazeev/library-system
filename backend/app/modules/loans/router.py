from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional

from app.modules.loans.schemas import (
    LoanResponse, LoanCreate, LoanReturn, LoanExtend,
    LoanDetailResponse, ActiveLoanResponse, UserLoanHistory,
    OverdueLoanResponse, LoanStatsResponse
)
from app.modules.loans.service import LoanService
from app.modules.loans.dependencies import get_loan_service
from app.modules.auth.dependencies import require_roles, get_current_active_user
from app.modules.auth.models import User

router = APIRouter()

# Reader endpoints (authenticated users)
@router.get("/my-loans", response_model=List[UserLoanHistory])
async def get_my_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    service: LoanService = Depends(get_loan_service)
):
    """Get current user's loan history"""
    return service.get_user_loans(current_user.id, skip, limit)

@router.get("/my-active-loans", response_model=List[ActiveLoanResponse])
async def get_my_active_loans(
    current_user: User = Depends(get_current_active_user),
    service: LoanService = Depends(get_loan_service)
):
    """Get current user's active loans"""
    return service.get_user_active_loans(current_user.id)

@router.get("/my-borrow-status")
async def check_my_borrow_status(
    current_user: User = Depends(get_current_active_user),
    service: LoanService = Depends(get_loan_service)
):
    """Check if current user can borrow more books"""
    return service.check_user_can_borrow(current_user.id)

# Librarian and Admin endpoints
@router.get("/", response_model=List[LoanDetailResponse])
async def get_all_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get all loans (librarian and admin only)"""
    return service.get_all_loans(skip, limit)

@router.get("/active", response_model=List[ActiveLoanResponse])
async def get_active_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get all active loans (librarian and admin only)"""
    return service.get_active_loans(skip, limit)

@router.get("/overdue", response_model=List[OverdueLoanResponse])
async def get_overdue_loans(
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get all overdue loans (librarian and admin only)"""
    return service.get_overdue_loans()

@router.get("/stats", response_model=LoanStatsResponse)
async def get_loan_statistics(
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get loan statistics (librarian and admin only)"""
    return service.get_loan_statistics()

@router.get("/user/{user_id}", response_model=List[UserLoanHistory])
async def get_user_loans(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get loan history for a specific user (librarian and admin only)"""
    return service.get_user_loans(user_id, skip, limit)

@router.get("/copy/{copy_id}/history")
async def get_copy_loan_history(
    copy_id: int,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get loan history for a specific copy (librarian and admin only)"""
    return service.get_copy_loan_history(copy_id)

@router.get("/{loan_id}", response_model=LoanDetailResponse)
async def get_loan_by_id(
    loan_id: int,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Get loan details by ID (librarian and admin only)"""
    return service.get_loan_by_id(loan_id)

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_data: LoanCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Create a new loan (librarian and admin only)"""
    return service.create_loan(loan_data)

@router.post("/{loan_id}/return", response_model=LoanResponse)
async def return_loan(
    loan_id: int,
    return_data: Optional[LoanReturn] = None,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Return a loaned book (librarian and admin only)"""
    return service.return_loan(loan_id, return_data)

@router.post("/{loan_id}/extend", response_model=LoanResponse)
async def extend_loan(
    loan_id: int,
    extend_data: LoanExtend,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: LoanService = Depends(get_loan_service)
):
    """Extend loan due date (librarian and admin only)"""
    return service.extend_loan(loan_id, extend_data)

# Admin only endpoints
@router.post("/daily-process")
async def run_daily_overdue_process(
    current_user: User = Depends(require_roles(["admin"])),
    service: LoanService = Depends(get_loan_service)
):
    """Run daily overdue processing (admin only)"""
    return service.process_daily_overdue()