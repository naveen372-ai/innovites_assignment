from sqlalchemy import Column, Integer, String, Float
from database import Base

class CableDesign(Base):
    __tablename__ = "cable_designs"
    id = Column(Integer, primary_key=True, index=True)
    cable_type = Column(String)
    size = Column(Float)
    color = Column(String)
    cut_length = Column(Float)
    design_code = Column(String)

class DesignRequest(Base):
    __tablename__ = "design_requests"
    id = Column(Integer, primary_key=True, index=True)
    cable_type = Column(String)
    size = Column(Float)
    color = Column(String)
    cut_length = Column(Float)
    design_code = Column(String)
