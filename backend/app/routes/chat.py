from fastapi import APIRouter, HTTPException, Depends
from app.models.chat import ChatRequest, ChatResponse, ChatHistory
from app.services.chat_service import ChatService
from app.services.auth_service import AuthService
from app.database.supabase import SupabaseDB

router = APIRouter()
db = SupabaseDB()
chat_service = ChatService(db)
auth_service = AuthService(db)

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    current_user = Depends(auth_service.get_current_user)
):
    try:
        return await chat_service.process_message(chat_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=list[ChatHistory])
async def get_chat_history(
    user_id: str,
    limit: int = 10,
    current_user = Depends(auth_service.get_current_user)
):
    try:
        return await chat_service.get_history(user_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))