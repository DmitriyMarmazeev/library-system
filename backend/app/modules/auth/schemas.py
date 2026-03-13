from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^\+?[0-9]{10,15}$')

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    password_confirm: str
    
    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    roles: List[RoleResponse] = []
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None

class RefreshToken(BaseModel):
    refresh_token: str