from sqlalchemy import Column, String, Boolean, DateTime, LargeBinary
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class BiometricTemplate(Base):
    """
    Stores ENCRYPTED embeddings only. Raw images are NEVER stored.
    """
    __tablename__ = "biometric_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True, index=True, nullable=False)
    
    # Encrypted 128-d or 512-d embeddings
    face_embedding_encrypted = Column(LargeBinary) # AES-256 encrypted vector
    fingerprint_template_encrypted = Column(LargeBinary)
    
    # Metadata
    algorithm_version = Column(String) # e.g. "DeepFace-V2"
    encryption_key_id = Column(String) # KMS Key ID
    
    # Liveness verification
    last_liveness_score = Column(float)
    is_liveness_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
