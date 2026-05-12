from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import enum
import uuid

class UserRole(str, enum.Enum):
    CEC = "chief_election_commissioner"
    EC = "election_commissioner"
    CEO = "state_chief_electoral_officer"
    DEO = "district_election_officer"
    RO = "returning_officer"
    ARO = "assistant_returning_officer"
    BLO = "booth_level_officer"
    OBSERVER = "observer"
    AUDITOR = "auditor"
    VOTER = "voter"

class ScopeType(str, enum.Enum):
    NATIONAL = "national"
    STATE = "state"
    DISTRICT = "district"
    PC = "parliamentary_constituency"
    AC = "assembly_constituency"
    BOOTH = "polling_booth"

class User(BaseModel):
    """
    Core Authentication & Authorization model.
    """
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    
    # RBAC
    role = Column(Enum(UserRole), default=UserRole.VOTER, nullable=False)
    
    # Strict Geographic Scoping (Replaces loose text fields)
    scope_type = Column(Enum(ScopeType), nullable=True) # Defines the level of access
    scope_id = Column(String, nullable=True) # Foreign key to the respective geography table based on scope_type

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Audit & Security tracking
    last_login = Column(DateTime(timezone=True))
    last_login_ip = Column(String)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True))
    
    # MFA & Session Management
    mfa_enabled = Column(Boolean, default=False)
    totp_secret = Column(String, nullable=True) # For Google Authenticator/TOTP
    refresh_token = Column(String, nullable=True) # For session invalidation
