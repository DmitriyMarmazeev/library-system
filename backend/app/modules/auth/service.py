from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException, status

from app.modules.auth.repository import UserRepository, RoleRepository
from app.modules.auth.schemas import UserCreate, UserLogin
from app.core.security import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token
)
from app.core.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
    
    def register_user(self, user_data: UserCreate):
        # Check if user exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create user
        user_dict = user_data.dict(exclude={'password', 'password_confirm'})
        user_dict['password_hash'] = get_password_hash(user_data.password)
        
        new_user = self.user_repo.create(user_dict)
        
        # Assign default reader role
        reader_role = self.role_repo.get_by_name("reader")
        if reader_role:
            self.user_repo.add_role(new_user, reader_role)
        
        # Generate tokens
        access_token = create_access_token({"sub": str(new_user.id)})
        refresh_token = create_refresh_token({"sub": str(new_user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def login_user(self, login_data: UserLogin):
        # Find user by email
        user = self.user_repo.get_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Verify password
        if not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def refresh_token(self, refresh_token: str):
        from jose import JWTError, jwt
        
        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if user_id is None or token_type != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Check if user exists and is active
        user = self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Generate new tokens
        access_token = create_access_token({"sub": str(user.id)})
        new_refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    
    def initialize_roles(self):
        """Initialize default roles in the system"""
        return self.role_repo.get_or_create_default_roles()