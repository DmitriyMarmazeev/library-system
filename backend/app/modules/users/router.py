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

# Admin only endpoints
@router.get("/", response_model=List[UserResponse])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Get all users (admin only)"""
    return service.get_all_users(skip, limit)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Create a new user (admin only)"""
    return service.create_user(user_data)

# Endpoints accessible by admin or the user themselves
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user

@router.get("/search", response_model=List[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1),
    current_user: User = Depends(require_roles(["admin", "librarian"])),
    service: UserService = Depends(get_user_service)
):
    """Search users by name or email (admin and librarian only)"""
    return service.search_users(q)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Get user by ID (admin or the user themselves)"""
    return service.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Update user (admin or the user themselves)"""
    return service.update_user(user_id, user_data)

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=False, require_admin=True)),
    service: UserService = Depends(get_user_service)
):
    """Delete user (admin only, cannot delete yourself)"""
    return service.delete_user(user_id)

@router.post("/{user_id}/change-password")
async def change_password(
    user_id: int,
    password_data: PasswordChange,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Change user password (admin or the user themselves)"""
    return service.change_password(user_id, password_data)

@router.post("/{user_id}/roles")
async def add_role_to_user(
    user_id: int,
    role_data: UserRoleUpdate,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Add role to user (admin only)"""
    if role_data.action == "add":
        return service.add_role(user_id, role_data.role_name)
    elif role_data.action == "remove":
        return service.remove_role(user_id, role_data.role_name)

@router.get("/{user_id}/roles")
async def get_user_roles(
    user_id: int,
    permission_checker = Depends(UserPermissionChecker(allow_self=True)),
    service: UserService = Depends(get_user_service)
):
    """Get user roles (admin or the user themselves)"""
    return service.get_user_roles(user_id)

@router.post("/{user_id}/toggle-active", response_model=UserResponse)
async def toggle_user_active(
    user_id: int,
    admin: User = Depends(require_roles(["admin"])),
    service: UserService = Depends(get_user_service)
):
    """Toggle user active status (admin only)"""
    return service.toggle_user_active(user_id)