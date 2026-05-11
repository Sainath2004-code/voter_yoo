from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
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

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(UserRole), default=UserRole.VOTER)
    
    # Geographic Scoping
    state_code = Column(String, index=True) # For CEO/State Admin
    district_code = Column(String, index=True) # For DEO
    constituency_id = Column(String, index=True) # For RO/ARO
    booth_no = Column(Integer) # For BLO

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Audit tracking
    last_login = Column(DateTime(timezone=True))
    
    # Biometric status
    has_face_enrolled = Column(Boolean, default=False)
    has_fingerprint_enrolled = Column(Boolean, default=False)
