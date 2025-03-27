from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from app.models.document import Document, DocumentCreate, DocumentSearch
from app.database.supabase import SupabaseDB
from app.config.settings import Settings

settings = Settings()
sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')

class RAGService:
    def __init__(self, db: SupabaseDB):
        self.db = db

    async def process_document(self, file_content: str, user_id: str) -> Document:
        # Extract text from file (assuming it's already text for now)
        # TODO: Add support for different file types (PDF, DOCX, etc.)
        
        document = await self.db.add_document(
            user_id=user_id,
            title="Sample Document",  # TODO: Extract from file
            content=file_content,
            source_type="file"
        )

        # Generate chunks and embeddings
        chunks = self._create_chunks(file_content)
        await self.db.add_document_chunks(document["id"], chunks)

        return document

    async def get_user_documents(self, user_id: str) -> List[Document]:
        return await self.db.get_user_documents(user_id)

    async def search_similar_chunks(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        # Generate query embedding using sentence transformer
        query_embedding = sentence_transformer.encode(query).tolist()
        
        return await self.db.search_similar_chunks(
            user_id=user_id,
            query_embedding=query_embedding,
            limit=settings.max_search_results
        )

    def _create_chunks(self, text: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        # Split text into chunks
        words = text.split()
        chunks = []
        current_chunk = []
        current_size = 0

        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1  # +1 for space

            if current_size >= chunk_size:
                chunk_text = " ".join(current_chunk)
                chunks.append({
                    "content": chunk_text,
                    "embedding": sentence_transformer.encode(chunk_text).tolist()
                })
                current_chunk = []
                current_size = 0

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "content": chunk_text,
                "embedding": sentence_transformer.encode(chunk_text).tolist()
            })

        return chunks 