from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.auth.models import User, Role

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, user_data: dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update(self, user_id: int, user_data: dict) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
    
    def add_role(self, user: User, role: Role) -> User:
        if role not in user.roles:
            user.roles.append(role)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def remove_role(self, user: User, role: Role) -> User:
        if role in user.roles:
            user.roles.remove(role)
            self.db.commit()
            self.db.refresh(user)
        return user

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_name(self, name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == name).first()
    
    def get_or_create_default_roles(self) -> List[Role]:
        default_roles = [
            {"name": "reader", "description": "Обычный читатель"},
            {"name": "librarian", "description": "Библиотекарь"},
            {"name": "admin", "description": "Администратор системы"}
        ]
        
        roles = []
        for role_data in default_roles:
            role = self.get_by_name(role_data["name"])
            if not role:
                role = Role(**role_data)
                self.db.add(role)
                roles.append(role)
            else:
                roles.append(role)
        
        self.db.commit()
        return roles