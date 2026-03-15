from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.users.models import User, Role

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
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
                if value is not None:
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
    
    def get_active_users(self) -> List[User]:
        return self.db.query(User).filter(User.is_active == True).all()
    
    def search_users(self, query: str) -> List[User]:
        search_term = f"%{query}%"
        return self.db.query(User).filter(
            (User.first_name.ilike(search_term)) |
            (User.last_name.ilike(search_term)) |
            (User.email.ilike(search_term))
        ).limit(20).all()

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_name(self, name: str) -> Optional[Role]:
        return self.db.query(Role).filter(Role.name == name).first()
    
    def get_all(self) -> List[Role]:
        return self.db.query(Role).all()
    
    def add_role_to_user(self, user: User, role_name: str) -> User:
        role = self.get_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' not found")
        
        if role not in user.roles:
            user.roles.append(role)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def remove_role_from_user(self, user: User, role_name: str) -> User:
        role = self.get_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' not found")
        
        if role in user.roles:
            user.roles.remove(role)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_user_roles(self, user: User) -> List[Role]:
        return user.roles