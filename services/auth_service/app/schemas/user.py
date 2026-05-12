from typing import Optional
from pydantic import BaseModel, EmailStr
from shared.models.user import UserRole
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None
    role: Optional[UserRole] = UserRole.VOTER
    scope_type: Optional[str] = None
    scope_id: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Additional properties to return via API
class UserResponse(UserBase):
    id: str
    is_verified: bool
    created_at: datetime
    has_face_enrolled: bool
    has_fingerprint_enrolled: bool

    class Config:
        from_attributes = True
