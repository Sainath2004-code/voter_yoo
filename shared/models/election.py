from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Date, Boolean
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import enum
import uuid

class ElectionType(str, enum.Enum):
    LOK_SABHA = "lok_sabha"
    VIDHAN_SABHA = "vidhan_sabha"
    BY_ELECTION = "by_election"

class ElectionStatus(str, enum.Enum):
    NOTIFICATION = "notification"
    NOMINATION = "nomination"
    SCRUTINY = "scrutiny"
    WITHDRAWAL = "withdrawal"
    CAMPAIGN = "campaign"
    POLLING = "polling"
    COUNTING = "counting"
    RESULTS = "results"
    ARCHIVED = "archived"

class Election(BaseModel):
    """
    Workflow-driven Election Lifecycle model.
    """
    __tablename__ = "elections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    type = Column(Enum(ElectionType), nullable=False)
    status = Column(Enum(ElectionStatus), default=ElectionStatus.NOTIFICATION, nullable=False)
    
    # Workflow Timelines
    notification_date = Column(Date)
    nomination_start_date = Column(Date)
    nomination_end_date = Column(Date)
    scrutiny_date = Column(Date)
    withdrawal_date = Column(Date)
    polling_date = Column(Date)
    counting_date = Column(Date)
    
    # Relationships
    candidates = relationship("Candidate", back_populates="election")
    phases = relationship("ElectionPhase", back_populates="election")

class ElectionPhase(BaseModel):
    __tablename__ = "election_phases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    election_id = Column(String, ForeignKey("elections.id"), nullable=False)
    phase_number = Column(String, nullable=False)
    polling_date = Column(Date, nullable=False)
    
    election = relationship("Election", back_populates="phases")

class PoliticalParty(BaseModel):
    __tablename__ = "political_parties"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    abbreviation = Column(String, nullable=False, unique=True)
    symbol_url = Column(String)
    is_national = Column(Boolean, default=False)
    
    candidates = relationship("Candidate", back_populates="party")

class CandidateStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class Candidate(BaseModel):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    election_id = Column(String, ForeignKey("elections.id"), nullable=False)
    party_id = Column(String, ForeignKey("political_parties.id"), nullable=True) # Independent candidates might have no party
    
    # The constituency they are contesting from (Could be LS or VS based on Election type)
    # Using a generic scope ID since a candidate contests exactly one constituency per election
    constituency_id = Column(String, nullable=False) 
    constituency_type = Column(String, nullable=False) # 'LS' or 'VS'
    
    # Candidate details
    voter_profile_id = Column(String, ForeignKey("voter_profiles.id"), nullable=False) # Must be a registered voter
    affidavit_url = Column(String)
    status = Column(Enum(CandidateStatus), default=CandidateStatus.PENDING)
    
    # Relationships
    election = relationship("Election", back_populates="candidates")
    party = relationship("PoliticalParty", back_populates="candidates")
    voter_profile = relationship("VoterProfile")
