from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from app.models.document import Document, DocumentCreate, DocumentSearch
from app.services.rag_service import RAGService
from app.services.auth_service import AuthService
from app.database.supabase import SupabaseDB

router = APIRouter()
db = SupabaseDB()
rag_service = RAGService(db)
auth_service = AuthService(db)

@router.post("/upload", response_model=Document)
async def upload_document(
    file: UploadFile = File(...),
    current_user = Depends(auth_service.get_current_user)
):
    try:
        return await rag_service.process_document(file, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[Document])
async def get_user_documents(
    user_id: str,
    current_user = Depends(auth_service.get_current_user)
):
    try:
        return await rag_service.get_user_documents(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_documents(
    search: DocumentSearch,
    current_user = Depends(auth_service.get_current_user)
):
    try:
        return await rag_service.search_documents(search)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))