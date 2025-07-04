from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from models import DesignRequest, ProductEnquiry
from schemas import ChatInput, DesignRequestOut, ProductEnquiryOut
from services import handle_enquiry_chat, handle_design_chat
from database import get_db

router = APIRouter()

@router.post("/enquiry/chat")
async def cable_enquiry_chat(input: ChatInput):
    return handle_enquiry_chat(input.user_id, input.message)

@router.post("/design/chat")
async def cable_design_chat(input: ChatInput):
    return handle_design_chat(input.user_id, input.message)

@router.get("/enquiry-requests", response_model=List[DesignRequestOut])
def list_design_requests(db: Session = Depends(get_db)):
    return db.query(DesignRequest).all()

@router.get("/product-enquiries", response_model=List[ProductEnquiryOut])
def list_product_enquiries(db: Session = Depends(get_db)):
    return db.query(ProductEnquiry).all()
