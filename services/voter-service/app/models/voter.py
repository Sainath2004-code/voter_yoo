from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, JSON
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class VoterProfile(Base):
    __tablename__ = "voter_profiles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, unique=True, index=True, nullable=False)
    
    # ECI Specifics
    epic_number = Column(String, unique=True, index=True, nullable=True) # Generated after approval
    part_no = Column(Integer)
    serial_no = Column(Integer)
    
    # Personal Info (India Specific)
    full_name = Column(String, nullable=False)
    father_name = Column(String)
    mother_name = Column(String)
    spouse_name = Column(String)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String)
    
    # Address Info (Geo Hierarchy)
    state_code = Column(String, nullable=False)
    district_code = Column(String, nullable=False)
    taluk_name = Column(String)
    pincode = Column(String, nullable=False)
    
    # Assembly & Parliamentary Mapping
    vidhan_sabha_id = Column(String, index=True) # MLA Constituency
    lok_sabha_id = Column(String, index=True)   # MP Constituency
    polling_booth_id = Column(String, index=True)
    
    # Identity (DPDP Compliant)
    aadhaar_masked = Column(String) # Store only last 4 digits (e.g. XXXX-XXXX-1234)
    aadhaar_vault_ref = Column(String) # Reference to secure vault (not stored in DB)
    
    # Verification Status
    is_verified = Column(Boolean, default=False)
    verification_status = Column(String, default="pending") # pending, approved, rejected
    rejection_reason = Column(String)
    
    # AI/OCR Metadata
    kyc_metadata = Column(JSON) 
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
