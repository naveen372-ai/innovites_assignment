from pydantic import BaseModel

class ChatInput(BaseModel):
    user_id: str
    message: str
