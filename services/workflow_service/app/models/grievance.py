from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Text, Integer
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import enum
import uuid

class GrievanceStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    CATEGORIZED = "categorized"
    ASSIGNED = "assigned"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Grievance(BaseModel):
    """
    ECI Complaint / Grievance lifecycle model.
    """
    __tablename__ = "grievances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False) # The citizen who filed it
    
    category = Column(String, nullable=False) # e.g. 'Voter List', 'Booth Issue', 'MCC Violation'
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    status = Column(Enum(GrievanceStatus), default=GrievanceStatus.SUBMITTED)
    
    # Geographic Scope (Where the issue happened)
    scope_type = Column(String) # 'booth', 'ac', 'district'
    scope_id = Column(String)
    
    # Assignments
    assigned_officer_id = Column(String, nullable=True)
    
    # SLA & Feedback
    sla_deadline = Column(DateTime(timezone=True))
    resolution_details = Column(Text)
    citizen_feedback_score = Column(Integer) # 1-5
