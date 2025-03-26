from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.user import UserCreate, User, Token
from app.services.auth_service import AuthService
from app.database.supabase import SupabaseDB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = SupabaseDB()
auth_service = AuthService(db)

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    try:
        return await auth_service.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return await auth_service.authenticate_user(form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user