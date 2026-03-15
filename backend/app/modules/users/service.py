from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.modules.users.repository import UserRepository, RoleRepository
from app.modules.users.schemas import UserCreate, UserUpdate, PasswordChange
from app.core.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
    
    def get_user_by_id(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    
    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.user_repo.get_all(skip, limit)
    
    def create_user(self, user_data: UserCreate):
        # Check if user exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create user
        user_dict = user_data.dict(exclude={'password'})
        user_dict['password_hash'] = get_password_hash(user_data.password)
        
        new_user = self.user_repo.create(user_dict)
        
        # Assign default reader role
        try:
            self.role_repo.add_role_to_user(new_user, "reader")
        except ValueError:
            # Role doesn't exist, but user was created
            pass
        
        return new_user
    
    def update_user(self, user_id: int, user_data: UserUpdate):
        user = self.get_user_by_id(user_id)
        
        # Check if email is being changed and is unique
        if user_data.email and user_data.email != user.email:
            existing = self.user_repo.get_by_email(user_data.email)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )
        
        update_dict = user_data.dict(exclude_unset=True)
        updated_user = self.user_repo.update(user_id, update_dict)
        
        return updated_user
    
    def delete_user(self, user_id: int):
        # Prevent deleting yourself? This should be handled at router level
        user = self.get_user_by_id(user_id)
        
        # Soft delete or hard delete? Using hard delete for now
        deleted = self.user_repo.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deleted successfully"}
    
    def change_password(self, user_id: int, password_data: PasswordChange):
        user = self.get_user_by_id(user_id)
        
        # Verify current password
        if not verify_password(password_data.current_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new passwords match
        password_data.validate_passwords_match()
        
        # Update password
        user.password_hash = get_password_hash(password_data.new_password)
        self.db.commit()
        
        return {"message": "Password changed successfully"}
    
    def add_role(self, user_id: int, role_name: str):
        user = self.get_user_by_id(user_id)
        
        try:
            updated_user = self.role_repo.add_role_to_user(user, role_name)
            return updated_user
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    
    def remove_role(self, user_id: int, role_name: str):
        user = self.get_user_by_id(user_id)
        
        # Prevent removing the last admin role? This should be checked at router level
        try:
            updated_user = self.role_repo.remove_role_from_user(user, role_name)
            return updated_user
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    
    def get_user_roles(self, user_id: int):
        user = self.get_user_by_id(user_id)
        return user.roles
    
    def search_users(self, query: str):
        return self.user_repo.search_users(query)
    
    def toggle_user_active(self, user_id: int):
        user = self.get_user_by_id(user_id)
        user.is_active = not user.is_active
        self.db.commit()
        self.db.refresh(user)
        return user