from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Global HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Global validation exception handler"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Generic exception handler for unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )

# Custom exceptions
class BookNotAvailableError(Exception):
    """Raised when a book is not available for borrowing"""
    pass

class UserNotFoundError(Exception):
    """Raised when a user is not found"""
    pass

class BookNotFoundError(Exception):
    """Raised when a book is not found"""
    pass

class CopyNotFoundError(Exception):
    """Raised when a book copy is not found"""
    pass

class LoanNotFoundError(Exception):
    """Raised when a loan is not found"""
    pass

class LoanAlreadyClosedError(Exception):
    """Raised when trying to return an already returned book"""
    pass