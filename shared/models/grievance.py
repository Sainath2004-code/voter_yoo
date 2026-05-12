from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, JSON
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

class GrievanceCategory(str, enum.Enum):
    VOTER_REGISTRATION = "voter_registration"
    POLLING_BOOTH = "polling_booth"
    CANDIDATE_CONDUCT = "candidate_conduct"
    TECHNICAL_ISSUE = "technical_issue"
    FRAUD_REPORT = "fraud_report"

class Grievance(BaseModel):
    """
    Public Grievance Redressal (PGR) model for citizens to report issues.
    """
    __tablename__ = "grievances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    category = Column(Enum(GrievanceCategory), nullable=False)
    status = Column(Enum(GrievanceStatus), default=GrievanceStatus.SUBMITTED, nullable=False)
    
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Geography scope (where the issue occurred)
    state_id = Column(String, ForeignKey("states.id"))
    district_id = Column(String, ForeignKey("districts.id"))
    ac_id = Column(String, ForeignKey("assembly_constituencies.id"))
    
    # Assignment
    assigned_officer_id = Column(String, ForeignKey("users.id"))
    
    # SLA & Priority
    priority = Column(String, default="medium") # low, medium, high, emergency
    sla_deadline = Column(DateTime(timezone=True))
    
    # Outcomes
    resolution_notes = Column(Text)
    attachment_urls = Column(JSON) # Evidence documents
    
    user = relationship("User", foreign_keys=[user_id])
    assigned_officer = relationship("User", foreign_keys=[assigned_officer_id])
    state = relationship("State")
    district = relationship("District")
    assembly_constituency = relationship("AssemblyConstituency")
