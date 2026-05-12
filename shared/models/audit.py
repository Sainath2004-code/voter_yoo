from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from shared.models.base import BaseModel
import uuid

class AuditLog(BaseModel):
    """
    Immutable audit trail for all enterprise governance operations.
    """
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Actor Context
    actor_id = Column(String, index=True, nullable=False) # Officer or User
    actor_role = Column(String)
    
    # Operation Context
    action = Column(String, nullable=False) # e.g. 'VOTER_APPROVED', 'ELECTION_STARTED'
    resource = Column(String, nullable=False) # e.g. 'voter_profiles', 'elections'
    resource_id = Column(String)
    
    # State Change Data (JSONB)
    before_state = Column(JSON)
    after_state = Column(JSON)
    
    # Traceability
    correlation_id = Column(String, index=True) # To link multiple actions in one session/workflow
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Regional Scoping (Audit by jurisdiction)
    scope_type = Column(String) # 'state', 'district', 'booth'
    scope_id = Column(String)
