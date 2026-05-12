from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True) # Soft delete
    archived_at = Column(DateTime(timezone=True), nullable=True)

    def delete(self, db):
        """Soft delete the record."""
        self.deleted_at = func.now()
        db.add(self)
        db.commit()

    def archive(self, db):
        """Archive the record."""
        self.archived_at = func.now()
        db.add(self)
        db.commit()
