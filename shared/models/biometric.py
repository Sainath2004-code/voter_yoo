from sqlalchemy import Column, String, Boolean, DateTime, LargeBinary, Float, JSON, Integer
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import uuid

class BiometricTemplate(BaseModel):
    """
    Enterprise-grade Biometric Vault. Stores ONLY encrypted embeddings.
    Strictly follows DPDP and ECI security standards.
    """
    __tablename__ = "biometric_templates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True, index=True, nullable=False)
    
    # Encrypted Payload (AES-GCM or Fernet)
    # Never store raw fingerprint/face images.
    face_embedding_encrypted = Column(LargeBinary, nullable=True)
    fingerprint_template_encrypted = Column(LargeBinary, nullable=True)
    
    # Template Metadata
    algorithm_version = Column(String, nullable=False) # e.g., 'DeepFace-V4', 'FingerLib-3.1'
    embedding_dimension = Column(Integer, default=512)
    encryption_metadata = Column(JSON) # Stores Key ID, IV, and rotation date
    
    # Security & Integrity
    confidence_score = Column(Float) # Score from initial enrollment
    liveness_status = Column(String, default="verified") # verified, suspicious, failed
    liveness_metadata = Column(JSON) # Depth analysis, texture analysis results
    
    # Audit trail for the template itself
    last_verified_at = Column(DateTime(timezone=True))
    verification_count = Column(Integer, default=0)
    is_revoked = Column(Boolean, default=False)
    revocation_reason = Column(String)
