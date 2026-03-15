from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.users.service import UserService
from app.modules.auth.dependencies import get_current_active_user, require_roles
from app.modules.auth.models import User

async def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

async def get_current_user_with_admin_check(
    current_user: User = Depends(require_roles(["admin"]))
):
    """Ensure user is admin"""
    return current_user

async def validate_user_id(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    """Validate that user exists"""
    user = service.get_user_by_id(user_id)
    return user

class UserPermissionChecker:
    def __init__(self, allow_self: bool = True, require_admin: bool = False):
        self.allow_self = allow_self
        self.require_admin = require_admin
    
    async def __call__(
        self,
        user_id: int,
        current_user: User = Depends(get_current_active_user),
        service: UserService = Depends(get_user_service)
    ):
        # Check if user exists
        target_user = service.get_user_by_id(user_id)
        
        # Check permissions
        is_admin = any(role.name == "admin" for role in current_user.roles)
        is_self = current_user.id == user_id
        
        if self.require_admin and not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin privileges required"
            )
        
        if not self.allow_self and is_self:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not allowed on yourself"
            )
        
        if not is_admin and not is_self:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only access your own data"
            )
        
        return target_user