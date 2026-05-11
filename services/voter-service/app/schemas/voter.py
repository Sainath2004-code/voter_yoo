from typing import Optional, Any
from pydantic import BaseModel
from datetime import date, datetime

# Shared properties
class VoterBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    national_id: Optional[str] = None
    constituency_id: Optional[str] = None

# Properties to receive via API on creation
class VoterCreate(VoterBase):
    user_id: str
    first_name: str
    last_name: str
    date_of_birth: date
    national_id: str

# Properties to receive via API on update
class VoterUpdate(VoterBase):
    pass

# Additional properties to return via API
class VoterResponse(VoterBase):
    id: str
    user_id: str
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
