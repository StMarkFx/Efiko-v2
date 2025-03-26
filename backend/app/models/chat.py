from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    user_id: str
    message: str
    response: str

class ChatHistory(BaseModel):
    id: str
    user_id: str
    message: str
    response: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    response: str
    relevant_documents: Optional[list] = None 