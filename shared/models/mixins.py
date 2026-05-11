from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.sql import func
from datetime import datetime

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()

class AuditMixin:
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
