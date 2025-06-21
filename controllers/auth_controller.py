from fastapi import APIRouter, HTTPException
from schemas.user import UserRegister, UserLogin
from services.auth_service import register_user, authenticate_user

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post("/signup")
async def signup(user: UserRegister):
    created = await register_user(user)
    if not created:
        raise HTTPException(status_code=400, detail='User already exists')
    return created

@router.post("/login")
async def login(user: UserLogin):
    auth_data = await authenticate_user(user)
    if not auth_data:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return auth_data 