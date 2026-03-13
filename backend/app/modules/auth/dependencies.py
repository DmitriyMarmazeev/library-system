from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import List

from app.core.database import get_db
from app.core.config import settings
from app.modules.auth.repository import UserRepository
from app.modules.auth.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise credentials_exception
        
        token_data = TokenPayload(sub=user_id, type=token_type)
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(token_data.sub))
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user

def require_roles(allowed_roles: List[str]):
    """
    Dependency to check if user has required roles
    """
    async def role_checker(
        current_user = Depends(get_current_active_user)
    ):
        user_roles = [role.name for role in current_user.roles]
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker