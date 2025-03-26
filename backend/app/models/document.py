from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    content: str
    source_type: str
    source_url: Optional[str] = None

class DocumentCreate(DocumentBase):
    user_id: str

class Document(DocumentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    user_id: str

    class Config:
        from_attributes = True

class DocumentChunk(BaseModel):
    document_id: str
    content: str
    embedding: List[float]
    chunk_index: int

    class Config:
        from_attributes = True

class DocumentSearch(BaseModel):
    query: str
    limit: Optional[int] = 5
    threshold: Optional[float] = 0.7