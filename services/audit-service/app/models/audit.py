from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    service_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    actor_id = Column(String)
    actor_role = Column(String)
    resource_id = Column(String)
    resource_type = Column(String)
    
    # Payload details
    old_value = Column(JSON)
    new_value = Column(JSON)
    
    # Context
    ip_address = Column(String)
    user_agent = Column(String)
    request_id = Column(String)
    
    # Security
    digital_signature = Column(String) # For integrity verification
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
