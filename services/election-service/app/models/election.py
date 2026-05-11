from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import enum
import uuid

class ElectionType(str, enum.Enum):
    LOK_SABHA = "lok_sabha"
    VIDHAN_SABHA = "vidhan_sabha"
    BY_ELECTION = "by_election"
    LOCAL_BODY = "local_body"

class ElectionStatus(str, enum.Enum):
    NOTIFICATION = "notification"
    NOMINATION = "nomination"
    SCRUTINY = "scrutiny"
    CAMPAIGN = "campaign"
    POLLING = "polling"
    COUNTING = "counting"
    RESULTS = "results"
    COMPLETED = "completed"

class Election(Base):
    __tablename__ = "elections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(Enum(ElectionType), nullable=False)
    status = Column(Enum(ElectionStatus), default=ElectionStatus.NOTIFICATION)
    
    notification_date = Column(DateTime(timezone=True))
    polling_date = Column(DateTime(timezone=True))
    results_date = Column(DateTime(timezone=True))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Constituency(Base):
    __tablename__ = "constituencies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    state_code = Column(String, nullable=False)
    type = Column(String) # 'LS' or 'VS'
    is_reserved = Column(Boolean, default=False)
    reservation_type = Column(String) # 'SC', 'ST', 'GEN'

class PollingBooth(Base):
    __tablename__ = "polling_booths"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    constituency_id = Column(String, ForeignKey("constituencies.id"))
    booth_no = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # ECI Mapping
    blo_id = Column(String) # Reference to User in auth-service
    presiding_officer_id = Column(String)

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    election_id = Column(String, ForeignKey("elections.id"), nullable=False)
    constituency_id = Column(String, ForeignKey("constituencies.id"), nullable=False)
    
    full_name = Column(String, nullable=False)
    party_name = Column(String)
    symbol_url = Column(String)
    affidavit_url = Column(String) # Required for scrutiny
    
    status = Column(String, default="pending") # pending, accepted, rejected
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
