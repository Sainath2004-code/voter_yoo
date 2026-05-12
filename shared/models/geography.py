from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from shared.models.base import BaseModel
import uuid

class State(BaseModel):
    __tablename__ = "states"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True) # ISO or ECI code
    type = Column(String) # 'State' or 'UT'
    
    districts = relationship("District", back_populates="state")

class District(BaseModel):
    __tablename__ = "districts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state_id = Column(String, ForeignKey("states.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    
    state = relationship("State", back_populates="districts")
    parliamentary_constituencies = relationship("ParliamentaryConstituency", back_populates="district")

class ParliamentaryConstituency(BaseModel):
    __tablename__ = "parliamentary_constituencies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    district_id = Column(String, ForeignKey("districts.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    is_reserved = Column(Boolean, default=False)
    reservation_category = Column(String) # 'SC', 'ST', 'General'
    delimitation_version = Column(String)
    
    district = relationship("District", back_populates="parliamentary_constituencies")
    assembly_constituencies = relationship("AssemblyConstituency", back_populates="parliamentary_constituency")

class AssemblyConstituency(BaseModel):
    __tablename__ = "assembly_constituencies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pc_id = Column(String, ForeignKey("parliamentary_constituencies.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    is_reserved = Column(Boolean, default=False)
    reservation_category = Column(String)
    
    parliamentary_constituency = relationship("ParliamentaryConstituency", back_populates="assembly_constituencies")
    polling_booths = relationship("PollingBooth", back_populates="assembly_constituency")

class PollingBooth(BaseModel):
    __tablename__ = "polling_booths"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ac_id = Column(String, ForeignKey("assembly_constituencies.id"))
    booth_no = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Integer, default=1500)
    voter_count = Column(Integer, default=0)
    
    assembly_constituency = relationship("AssemblyConstituency", back_populates="polling_booths")
