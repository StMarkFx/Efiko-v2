from typing import List
from app.models.chat import ChatRequest, ChatResponse, ChatHistory
from app.services.rag_service import RAGService
from app.database.supabase import SupabaseDB

class ChatService:
    def __init__(self, db: SupabaseDB):
        self.db = db
        self.rag_service = RAGService(db)

    async def process_message(self, chat_request: ChatRequest) -> ChatResponse:
        # Get relevant documents using RAG
        relevant_docs = await self.rag_service.search_similar_chunks(
            chat_request.user_id,
            chat_request.message
        )

        # Generate response using the context from relevant documents
        response = await self._generate_response(chat_request.message, relevant_docs)

        # Save chat history
        await self.db.save_chat(
            chat_request.user_id,
            chat_request.message,
            response
        )

        return ChatResponse(
            response=response,
            relevant_documents=relevant_docs
        )

    async def get_history(self, user_id: str, limit: int = 10) -> List[ChatHistory]:
        return await self.db.get_chat_history(user_id, limit)

    async def _generate_response(self, message: str, context: List[dict]) -> str:
        # TODO: Implement actual response generation using an LLM
        # This is a placeholder implementation
        return f"Processed message: {message} with {len(context)} relevant documents"