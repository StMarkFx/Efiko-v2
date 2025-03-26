from supabase import create_client, Client
from app.config.settings import SUPABASE_URL, SUPABASE_KEY
from typing import List, Dict, Optional, Any
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseDB:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    def verify_setup(self) -> Dict[str, Any]:
        """Verify that all required tables and functions exist"""
        try:
            # Check if vector extension is enabled
            vector_ext = self.supabase.table('pg_extension').select('*').eq('extname', 'vector').execute()
            vector_enabled = len(vector_ext.data) > 0
            
            # Check if tables exist
            tables = self.supabase.table('information_schema.tables').select('table_name').eq('table_schema', 'public').execute()
            required_tables = {'users', 'chat_history', 'documents', 'document_chunks', 'user_documents'}
            existing_tables = {table['table_name'] for table in tables.data}
            missing_tables = required_tables - existing_tables
            
            # Check if match_documents function exists
            functions = self.supabase.table('information_schema.routines').select('routine_name').eq('routine_schema', 'public').execute()
            existing_functions = {func['routine_name'] for func in functions.data}
            match_documents_exists = 'match_documents' in existing_functions
            
            return {
                "vector_extension_enabled": vector_enabled,
                "required_tables": required_tables,
                "existing_tables": existing_tables,
                "missing_tables": missing_tables,
                "match_documents_function_exists": match_documents_exists,
                "setup_complete": vector_enabled and len(missing_tables) == 0 and match_documents_exists
            }
        except Exception as e:
            return {
                "error": str(e),
                "vector_extension_enabled": False,
                "required_tables": set(),
                "existing_tables": set(),
                "missing_tables": set(),
                "match_documents_function_exists": False,
                "setup_complete": False
            }

    def add_user(self, email: str, user_data: dict) -> Dict[str, Any]:
        try:
            response = self.supabase.table('users').insert(user_data).execute()
            return response.data[0]
        except Exception as e:
            raise Exception(f"Failed to add user: {str(e)}")
        
    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.supabase.table('users').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Failed to get user: {str(e)}")

    def save_chat(self, user_id: str, message: str, response: str) -> Dict[str, Any]:
        try:
            chat_data = {
                "user_id": user_id,
                "message": message,
                "response": response
            }
            response = self.supabase.table('chat_history').insert(chat_data).execute()
            return response.data[0]
        except Exception as e:
            raise Exception(f"Failed to save chat: {str(e)}")

    def get_chat_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table('chat_history')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Failed to get chat history: {str(e)}")

    def add_document(self, user_id: str, title: str, content: str, source_type: str, source_url: Optional[str] = None) -> Dict[str, Any]:
        try:
            # First insert the document
            document_data = {
                "title": title,
                "content": content,
                "source_type": source_type,
                "source_url": source_url
            }
            doc_response = self.supabase.table('documents').insert(document_data).execute()
            document = doc_response.data[0]

            # Then associate it with the user
            user_doc_data = {
                "user_id": user_id,
                "document_id": document['id']
            }
            self.supabase.table('user_documents').insert(user_doc_data).execute()

            return document
        except Exception as e:
            raise Exception(f"Failed to add document: {str(e)}")

    def add_document_chunks(self, document_id: str, chunks: List[Dict[str, any]]) -> List[Dict[str, Any]]:
        try:
            chunk_data = [
                {
                    "document_id": document_id,
                    "content": chunk["content"],
                    "embedding": chunk["embedding"].tolist() if isinstance(chunk["embedding"], np.ndarray) else chunk["embedding"],
                    "chunk_index": idx
                }
                for idx, chunk in enumerate(chunks)
            ]
            response = self.supabase.table('document_chunks').insert(chunk_data).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Failed to add document chunks: {str(e)}")

    def search_similar_chunks(self, user_id: str, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        try:
            # Using vector similarity search
            response = self.supabase.rpc(
                'match_documents',
                {
                    'query_embedding': query_embedding,
                    'match_threshold': 0.7,
                    'match_count': limit
                }
            ).execute()
            return response.data
        except Exception as e:
            raise Exception(f"Failed to search similar chunks: {str(e)}")

    def get_user_documents(self, user_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.supabase.table('documents')\
                .select('*')\
                .join('user_documents', 'documents.id=user_documents.document_id')\
                .eq('user_documents.user_id', user_id)\
                .execute()
            return response.data
        except Exception as e:
            raise Exception(f"Failed to get user documents: {str(e)}")
