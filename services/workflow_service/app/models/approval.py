from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import uuid

class ApprovalHistory(BaseModel):
    """
    Generic audit trail for any workflow approval (Voter Form 6, Candidate Nomination, etc).
    """
    __tablename__ = "approval_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    entity_type = Column(String, nullable=False) # 'voter_application', 'nomination', 'grievance'
    entity_id = Column(String, nullable=False)
    
    action = Column(String, nullable=False) # 'approve', 'reject', 'query', 'escalate'
    from_status = Column(String)
    to_status = Column(String)
    
    performed_by_id = Column(String, nullable=False) # Officer ID
    comments = Column(Text)
    
    # Contextual metadata (e.g. digital signature hash)
    metadata_json = Column(JSON)

class VerificationTask(BaseModel):
    """
    Represents an active task in a workflow queue.
    """
    __tablename__ = "verification_tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    
    assigned_role = Column(String, nullable=False) # e.g. 'BLO'
    assigned_scope_id = Column(String, nullable=False) # e.g. Booth ID
    
    priority = Column(String, default="normal") # normal, urgent, critical
    due_date = Column(DateTime(timezone=True))
    is_completed = Column(String, default="false")
