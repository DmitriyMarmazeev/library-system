from fastapi import APIRouter, Depends, Query, status
from typing import List

from app.modules.users.schemas import (
    UserResponse, UserCreate, UserUpdate, 
    UserRoleUpdate, PasswordChange
)
from app.modules.users.service import UserService
from app.modules.users.dependencies import (
    get_user_service, get_current_user_with_admin_check,
    UserPermissionChecker
)
from app.modules.auth.dependencies import require_roles, get_current_active_user
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
# Admin only endpoints
# ----------------------------------------------------------------

@router.get(
    "/",
    response_model=List[UserResponse],
    responses={
        200: {"description": "List of all users"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_all_users(
    skip: int = Query(0, ge=0, le=10_000),
    limit: int = Query(100, ge=1, le=1000),
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Get all users (admin only)"""
    return service.get_all_users(skip, limit)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created"},
        400: {"description": "Bad request – invalid input or user already exists"},
        409: {"description": "Conflict – user with this email already exists"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def create_user(
    user_data: UserCreate,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Create a new user (admin only)"""
    return service.create_user(user_data)


# ----------------------------------------------------------------
# Endpoints accessible by admin or the user themselves
# ----------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        200: {"description": "Current user information"},
        **AUTH_RESPONSES,
    }
)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user


@router.get(
    "/search",
    response_model=List[UserResponse],
    responses={
        200: {"description": "Search results"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def search_users(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: UserService = Depends(get_user_service)
):
    """Search users by name or email (admin and librarian only)"""
    return service.search_users(q)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        200: {"description": "User details"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_user_by_id(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Get user by ID (admin or the user themselves)"""
    return service.get_user_by_id(user_id)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    responses={
        200: {"description": "User updated"},
        400: {"description": "Bad request – duplicate email or other violation"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Update user (admin or the user themselves)"""
    return service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    responses={
        200: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def delete_user(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=False, require_admin=True)),
    service: UserService = Depends(get_user_service)
):
    """Delete user (admin only, cannot delete yourself)"""
    return service.delete_user(user_id)


@router.post(
    "/{user_id}/change-password",
    responses={
        200: {"description": "Password changed successfully"},
        400: {"description": "Bad request – incorrect current password or validation error"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def change_password(
    user_id: int,
    password_data: PasswordChange,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Change user password (admin or the user themselves)"""
    return service.change_password(user_id, password_data)


@router.post(
    "/{user_id}/roles",
    responses={
        200: {"description": "Role updated successfully"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        404: {"description": "User or role not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def add_role_to_user(
    user_id: int,
    role_data: UserRoleUpdate,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Add or remove role from user (admin only)"""
    if role_data.action == "add":
        return service.add_role(user_id, role_data.role_name)
    elif role_data.action == "remove":
        return service.remove_role(user_id, role_data.role_name)


@router.get(
    "/{user_id}/roles",
    responses={
        200: {"description": "List of user roles"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def get_user_roles(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Get user roles (admin or the user themselves)"""
    return service.get_user_roles(user_id)


@router.post(
    "/{user_id}/toggle-active",
    response_model=UserResponse,
    responses={
        200: {"description": "User active status toggled"},
        400: {"description": "Bad request – malformed body or invalid JSON"},
        404: {"description": "User not found"},
        **AUTH_RESPONSES,
        **VALIDATION_RESPONSE,
    }
)
async def toggle_user_active(
    user_id: int,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Toggle user active status (admin only)"""
    return service.toggle_user_active(user_id)