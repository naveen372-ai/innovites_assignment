from fastapi import APIRouter
from schemas import ChatInput
from services import handle_enquiry_chat, handle_design_chat

router = APIRouter()

@router.post("/enquiry/chat")
async def cable_enquiry_chat(input: ChatInput):
    return handle_enquiry_chat(input.user_id, input.message)

@router.post("/design/chat")
async def cable_design_chat(input: ChatInput):
    return handle_design_chat(input.user_id, input.message)
