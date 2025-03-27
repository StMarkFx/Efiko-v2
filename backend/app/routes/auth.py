from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.supabase import SupabaseDB
from backend.app.services.auth_service import AuthService
from app.models.auth import UserCreate, UserResponse, Token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = SupabaseDB()
auth_service = AuthService()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    try:
        # Check if user exists
        existing_user = await db.get_user(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user in Supabase
        user_data = {
            "email": user.email,
            "password": auth_service.get_password_hash(user.password),
            "full_name": user.full_name
        }
        new_user = await db.create_user(user_data)
        
        return UserResponse(
            id=new_user["id"],
            email=new_user["email"],
            full_name=new_user["full_name"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await db.get_user(form_data.username)
        if not user or not auth_service.verify_password(form_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        
        access_token = auth_service.create_access_token(data={"sub": user["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_email = auth_service.get_current_user(token)
        user = await db.get_user(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))