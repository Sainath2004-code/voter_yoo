from sqlalchemy import Column, String, DateTime, Enum, JSON, Text, ForeignKey
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import enum
import uuid

class ApplicationType(str, enum.Enum):
    FORM_6 = "form_6" # New Enrollment
    FORM_7 = "form_7" # Deletion
    FORM_8 = "form_8" # Correction

class ApplicationStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    BLO_VERIFICATION = "blo_verification"
    ERO_REVIEW = "ero_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EPIC_GENERATED = "epic_generated"

class VoterApplication(BaseModel):
    """
    Formal ECI Application (Form 6, 7, 8) with multi-level approval workflow.
    """
    __tablename__ = "voter_applications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    type = Column(Enum(ApplicationType), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED, nullable=False)
    
    # Hierarchical scope of the application (Relational)
    state_id = Column(String, ForeignKey("states.id"), nullable=False)
    district_id = Column(String, ForeignKey("districts.id"), nullable=False)
    ac_id = Column(String, ForeignKey("assembly_constituencies.id"), nullable=False)
    booth_id = Column(String, ForeignKey("polling_booths.id"), nullable=False)

    # Payload & Documents
    form_data = Column(JSON, nullable=False) # Stores all voter profile details
    document_hashes = Column(JSON) # IPFS or S3 hashes for proof docs
    
    # Workflow Assignment
    current_task_id = Column(String) # Link to active VerificationTask (to be implemented)
    assigned_officer_id = Column(String, ForeignKey("users.id")) # Current officer handling it
    
    # EPIC outcome
    generated_epic_number = Column(String, unique=True, index=True)

    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    assigned_officer = relationship("User", foreign_keys=[assigned_officer_id])
    state = relationship("State")
    district = relationship("District")
    assembly_constituency = relationship("AssemblyConstituency")
    polling_booth = relationship("PollingBooth")
