from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum
import uuid

class ApplicationType(str, enum.Enum):
    FORM_6 = "form_6" # New Enrollment
    FORM_7 = "form_7" # Deletion
    FORM_8 = "form_8" # Correction

class ApplicationStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    BLO_ASSIGNED = "blo_assigned"
    FIELD_VERIFIED = "field_verified"
    APPROVED = "approved"
    REJECTED = "rejected"
    EPIC_GENERATED = "epic_generated"

class VoterApplication(Base):
    __tablename__ = "voter_applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    type = Column(Enum(ApplicationType), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    
    # Data Payload
    form_data = Column(JSON, nullable=False)
    document_urls = Column(JSON)
    
    # BLO Verification
    blo_id = Column(String, index=True)
    blo_remarks = Column(String)
    field_verification_date = Column(DateTime(timezone=True))
    
    # Final Approval
    approved_by = Column(String) # RO or ARO
    approval_date = Column(DateTime(timezone=True))
    rejection_reason = Column(String)
    
    # EPIC Reference
    epic_number = Column(String, unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
