from fastapi import APIRouter, Depends, Query, status
from typing import List

from app.modules.copies.schemas import (
    CopyResponse, CopyCreate, CopyUpdate, CopyStatusUpdate,
    CopyBulkCreate, CopyBulkCreateResponse, CopyDetailResponse,
    CopyStatusEnum, CopyLoanHistory
)
from app.modules.copies.service import CopyService
from app.modules.copies.dependencies import get_copy_service
from app.modules.auth.dependencies import require_roles
from app.modules.auth.models import User

router = APIRouter()

# Общие блоки ответов
AUTH_RESPONSES = {
    401: {"description": "Not authenticated"},
    403: {"description": "Forbidden – insufficient permissions"},
}
VALIDATION_RESPONSE = {
    422: {"description": "Validation Error"}
}


# ----------------------------------------------------------------
# Public endpoints (any authenticated user)
# ----------------------------------------------------------------

@router.get(
    "/",
    response_model=List[CopyResponse],
    responses={
        200: {"description": "List of all copies"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_all_copies(
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: CopyService = Depends(get_copy_service)
):
    """Get all copies (authenticated users)"""
    return service.get_all_copies(skip, limit)


@router.get(
    "/by-book/{book_id}",
    response_model=List[CopyResponse],
    responses={
        200: {"description": "Copies of the specified book"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_copies_by_book(
    book_id: int,
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: CopyService = Depends(get_copy_service)
):
    """Get all copies of a specific book"""
    return service.get_copies_by_book(book_id, skip, limit)


@router.get(
    "/status/{status}",
    response_model=List[CopyResponse],
    responses={
        200: {"description": "Copies filtered by status"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_copies_by_status(
    status: CopyStatusEnum,
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: CopyService = Depends(get_copy_service)
):
    """Get copies by status"""
    return service.get_copies_by_status(status, skip, limit)


@router.get(
    "/search/location",
    responses={
        200: {"description": "Copies matching the location search"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def search_by_location(
    q: str = Query(..., min_length=1),
    service: CopyService = Depends(get_copy_service)
):
    """Search copies by location"""
    return service.search_by_location(q)


@router.get(
    "/book-summary/{book_id}",
    responses={
        200: {"description": "Summary of copies for the book"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
    }
)
async def get_book_copies_summary(
    book_id: int,
    service: CopyService = Depends(get_copy_service)
):
    """Get summary of copies for a book"""
    return service.get_book_copies_summary(book_id)


@router.get(
    "/{copy_id}",
    response_model=CopyDetailResponse,
    responses={
        200: {"description": "Copy details"},
        404: {"description": "Copy not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_copy_by_id(
    copy_id: int,
    service: CopyService = Depends(get_copy_service)
):
    """Get copy details by ID"""
    return service.get_copy_details(copy_id)


@router.get(
    "/{copy_id}/history",
    response_model=List[CopyLoanHistory],
    responses={
        200: {"description": "Loan history of the copy"},
        404: {"description": "Copy not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_copy_loan_history(
    copy_id: int,
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    service: CopyService = Depends(get_copy_service)
):
    """Get loan history for a specific copy"""
    return service.get_copy_loan_history(copy_id, skip, limit)


# ----------------------------------------------------------------
# Protected endpoints (librarian and admin only)
# ----------------------------------------------------------------

@router.post(
    "/",
    response_model=CopyResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Copy created"},
        400: {"description": "Bad request – invalid input or business rule violation"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_copy(
    copy_data: CopyCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: CopyService = Depends(get_copy_service)
):
    """Create a new copy (librarian and admin only)"""
    return service.create_copy(copy_data)


@router.post(
    "/bulk",
    response_model=CopyBulkCreateResponse,
    responses={
        200: {"description": "Bulk copies created"},
        400: {"description": "Bad request – invalid input or business rule violation"},
        404: {"description": "Book not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_copies_bulk(
    bulk_data: CopyBulkCreate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: CopyService = Depends(get_copy_service)
):
    """Create multiple copies at once (librarian and admin only)"""
    return service.create_copies_bulk(bulk_data)


@router.put(
    "/{copy_id}",
    response_model=CopyResponse,
    responses={
        200: {"description": "Copy updated"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        404: {"description": "Copy not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_copy(
    copy_id: int,
    copy_data: CopyUpdate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: CopyService = Depends(get_copy_service)
):
    """Update copy (librarian and admin only)"""
    return service.update_copy(copy_id, copy_data)


@router.patch(
    "/{copy_id}/status",
    response_model=CopyResponse,
    responses={
        200: {"description": "Copy status updated"},
        400: {"description": "Invalid status transition (e.g., copy already in that status)"},
        404: {"description": "Copy not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_copy_status(
    copy_id: int,
    status_update: CopyStatusUpdate,
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: CopyService = Depends(get_copy_service)
):
    """Update copy status (librarian and admin only)"""
    return service.update_copy_status(copy_id, status_update)


@router.delete(
    "/{copy_id}",
    responses={
        200: {"description": "Copy deleted successfully"},
        400: {"description": "Bad request – copy cannot be deleted (e.g., currently loaned)"},
        404: {"description": "Copy not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def delete_copy(
    copy_id: int,
    current_user: User = Depends(require_roles(["admin"])),
    service: CopyService = Depends(get_copy_service)
):
    """Delete copy (admin only)"""
    return service.delete_copy(copy_id)