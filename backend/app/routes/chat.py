from fastapi import APIRouter, HTTPException, Depends
from app.database.supabase import SupabaseDB
from app.services.auth import AuthService
from app.services.chat import ChatService
from app.models.chat import ChatMessage, ChatResponse
from typing import List

router = APIRouter()
db = SupabaseDB()
chat_service = ChatService()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    token: str = Depends(AuthService().get_current_user)
):
    try:
        # Get user's email from token
        user_email = AuthService().get_current_user(token)
        user = await db.get_user(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get relevant document chunks
        relevant_chunks = await chat_service.get_relevant_chunks(user["id"], message.content)
        
        # Generate response using Gemini
        response = await chat_service.generate_response(
            message.content,
            relevant_chunks
        )

        # Save chat history
        await db.save_chat(user["id"], message.content, response)

        return ChatResponse(
            message=response,
            relevant_chunks=relevant_chunks
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[ChatResponse])
async def get_chat_history(
    limit: int = 10,
    token: str = Depends(AuthService().get_current_user)
):
    try:
        user_email = AuthService().get_current_user(token)
        user = await db.get_user(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        history = await db.get_chat_history(user["id"], limit)
        return [
            ChatResponse(
                message=chat["response"],
                relevant_chunks=[]  # We don't store chunks in history
            )
            for chat in history
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))