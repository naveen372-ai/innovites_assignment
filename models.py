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

class Product(Base):
    __tablename__ = "products"

    product_code = Column(String, primary_key=True)
    cable_name = Column(String)
    num_cores = Column(Integer)
    conductor_type = Column(String)
    area = Column(Float)
    customer_code = Column(String)
    quantity = Column(Integer)
    length = Column(Float)


class ProductEnquiry(Base):
    __tablename__ = "product_enquiries"

    id = Column(Integer, primary_key=True, index=True)
    cable_name = Column(String)
    num_cores = Column(Integer)
    conductor_type = Column(String)
    area = Column(Float)
    customer_code = Column(String)
    quantity = Column(Integer)
    length = Column(Float)
    product_code = Column(String)
