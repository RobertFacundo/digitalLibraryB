from models.user import User
from schemas.user import UserRegister, UserLogin
from utils.auth_utils import hash_password, verify_password, create_access_token
from sqlalchemy.future import select
from database import database
from fastapi import HTTPException

async def register_user(user: UserRegister):
    query = select(User).where(User.username == user.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        return None
    
    hashed = hash_password(user.password)
    query = User.__table__.insert().values(username=user.username, hashed_password=hashed)
    await database.execute(query)
    return {"username": user.username}

async def authenticate_user(user: UserLogin):
    query = select(User).where(User.username == user.username)
    db_user = await database.fetch_one(query)
    if not db_user:
        return None
    if not verify_password(user.password, db_user["hashed_password"]):
        return None
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}