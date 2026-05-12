from sqlalchemy import Column, String, DateTime, Enum, JSON, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import enum
import uuid

class TaskType(str, enum.Enum):
    VOTER_VERIFICATION = "voter_verification"
    CANDIDATE_SCRUTINY = "candidate_scrutiny"
    GRIEVANCE_RESOLUTION = "grievance_resolution"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class VerificationTask(BaseModel):
    """
    Specific actionable task assigned to an officer as part of a workflow.
    """
    __tablename__ = "verification_tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(Enum(TaskType), nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    
    # Links to the actual entity being verified
    entity_id = Column(String, nullable=False, index=True) # e.g. application_id or candidate_id
    entity_type = Column(String, nullable=False) # 'voter_application', 'candidate_affidavit'
    
    # Assignment
    assigned_officer_id = Column(String, ForeignKey("users.id"), index=True)
    
    # Geography constraints (inherited from entity)
    scope_type = Column(String) 
    scope_id = Column(String)
    
    # Task state
    status = Column(String, default="pending") # pending, in_progress, completed, failed
    due_date = Column(DateTime(timezone=True))
    
    # Results
    comments = Column(Text)
    verification_payload = Column(JSON) # Field-by-field verification results
    
    assigned_officer = relationship("User")

class ApprovalHistory(BaseModel):
    """
    Immutable audit trail of all workflow approvals/rejections.
    """
    __tablename__ = "approval_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    entity_id = Column(String, nullable=False, index=True)
    entity_type = Column(String, nullable=False)
    
    action = Column(String, nullable=False) # approved, rejected, queried, escalated
    previous_status = Column(String)
    new_status = Column(String)
    
    officer_id = Column(String, ForeignKey("users.id"), nullable=False)
    comments = Column(Text)
    
    # Metadata
    ip_address = Column(String)
    user_agent = Column(String)
    
    officer = relationship("User")

class WorkflowTransition(BaseModel):
    """
    Configuration table for valid workflow state transitions.
    """
    __tablename__ = "workflow_transitions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_name = Column(String, nullable=False) # 'voter_registration', 'election_lifecycle'
    from_status = Column(String, nullable=False)
    to_status = Column(String, nullable=False)
    required_role = Column(String) # Role required to trigger this transition
    
    is_active = Column(Integer, default=1)
