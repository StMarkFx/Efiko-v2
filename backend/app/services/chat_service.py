import google.generativeai as genai
from app.config.settings import Settings
from app.database.supabase import SupabaseDB
from sentence_transformers import SentenceTransformer
import numpy as np

settings = Settings()
db = SupabaseDB()

# Initialize Gemini
genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

# Initialize sentence transformer for embeddings
sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

class ChatService:
    async def get_relevant_chunks(self, user_id: str, query: str) -> list:
        try:
            # Generate embedding for the query
            query_embedding = sentence_transformer.encode(query).tolist()
            
            # Search for relevant chunks
            relevant_chunks = await db.search_similar_chunks(
                user_id,
                query_embedding,
                limit=settings.max_search_results
            )
            
            return relevant_chunks
        except Exception as e:
            print(f"Error getting relevant chunks: {str(e)}")
            return []

    async def generate_response(self, message: str, relevant_chunks: list) -> str:
        try:
            # Prepare context from relevant chunks
            context = "\n".join([chunk["content"] for chunk in relevant_chunks])
            
            # Prepare prompt
            prompt = f"""Context information is below.
---------------------
{context}
---------------------
Given the context information and no other information, answer the following question:
{message}

If the context doesn't contain enough information to answer the question, say "I don't have enough information to answer that question."""

            # Generate response using Gemini
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while processing your request." 