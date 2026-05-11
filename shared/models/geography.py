from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import uuid

class StateUT(Base):
    __tablename__ = "states_uts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, unique=True)
    code = Column(String, nullable=False, unique=True) # ISO or ECI code
    type = Column(String) # 'State' or 'UT'
    
    districts = relationship("District", back_populates="state")

class District(Base):
    __tablename__ = "districts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state_id = Column(String, ForeignKey("states_uts.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    
    state = relationship("StateUT", back_populates="districts")
    taluks = relationship("Taluk", back_populates="district")

class Taluk(Base):
    __tablename__ = "taluks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    district_id = Column(String, ForeignKey("districts.id"))
    name = Column(String, nullable=False)
    
    district = relationship("District", back_populates="taluks")

class LokSabhaConstituency(Base):
    __tablename__ = "lok_sabha_constituencies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state_id = Column(String, ForeignKey("states_uts.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    is_reserved = Column(String) # 'SC', 'ST', 'General'

class VidhanSabhaConstituency(Base):
    __tablename__ = "vidhan_sabha_constituencies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    state_id = Column(String, ForeignKey("states_uts.id"))
    district_id = Column(String, ForeignKey("districts.id"))
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    ls_constituency_id = Column(String, ForeignKey("lok_sabha_constituencies.id"))

class PollingBooth(Base):
    __tablename__ = "polling_booths"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    vs_constituency_id = Column(String, ForeignKey("vidhan_sabha_constituencies.id"))
    booth_no = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    blo_id = Column(String) # Link to User model
