from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserRegister, UserLogin
from services.auth_service import register_user, authenticate_user
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post("/signup")
async def signup(user: UserRegister, db: AsyncSession = Depends(get_async_db)):
    created = await register_user(user, db)
    if not created:
        raise HTTPException(status_code=400, detail='User already exists')
    return created

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    auth_data = await authenticate_user(user, db)
    if not auth_data:
        raise HTTPException(status_code=401, detail="invalid credentials")
    return auth_data 