from pydantic import BaseModel

class ChatInput(BaseModel):
    user_id: str
    message: str

class DesignRequestOut(BaseModel):
    cable_type: str
    size: float
    color: str
    cut_length: float
    design_code: str

    class Config:
        orm_mode = True

from pydantic import BaseModel

class ProductEnquiryOut(BaseModel):
    id: int
    cable_name: str
    num_cores: int
    conductor_type: str
    area: float
    customer_code: str
    quantity: int
    length: float
    product_code: str

    class Config:
        orm_mode = True
