from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.schemas import UserCreate, UserLogin, Token, RefreshToken, UserResponse
from app.modules.auth.service import AuthService
from app.modules.auth.dependencies import get_current_active_user

router = APIRouter()

# Общие блоки ответов
AUTH_RESPONSES = {
    401: {"description": "Not authenticated"},
    403: {"description": "Forbidden – insufficient permissions"},
}
VALIDATION_RESPONSE = {
    422: {"description": "Validation Error"}
}


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User successfully registered"},
        400: {"description": "Bad request – invalid input"},
        409: {"description": "Conflict – user already exists"},
        **VALIDATION_RESPONSE,
    }
)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)


@router.post(
    "/login",
    response_model=Token,
    responses={
        200: {"description": "Successful login – returns access and refresh tokens"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        401: {"description": "Invalid email or password"},
        **VALIDATION_RESPONSE,
    }
)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login and get access token
    """
    auth_service = AuthService(db)
    return auth_service.login_user(login_data)


@router.post(
    "/refresh",
    response_model=Token,
    responses={
        200: {"description": "New access token generated"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        401: {"description": "Invalid or expired refresh token"},
        **VALIDATION_RESPONSE,
    }
)
async def refresh(
    refresh_data: RefreshToken,
    db: Session = Depends(get_db)
):
    """
    Get new access token using refresh token
    """
    auth_service = AuthService(db)
    return auth_service.refresh_token(refresh_data.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        200: {"description": "Current user information"},
        **AUTH_RESPONSES,
    }
)
async def get_current_user_info(
    current_user = Depends(get_current_active_user)
):
    """
    Get current authenticated user information
    """
    return current_user


@router.post(
    "/init-roles",
    responses={
        200: {"description": "Roles initialized successfully"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        **AUTH_RESPONSES,
    }
)
async def initialize_roles(
    db: Session = Depends(get_db)
):
    """
    Initialize default roles in the system
    """
    auth_service = AuthService(db)
    roles = auth_service.initialize_roles()
    return {"message": "Roles initialized", "roles": [role.name for role in roles]}