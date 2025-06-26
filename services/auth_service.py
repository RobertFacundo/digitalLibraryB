from models.user import User
from schemas.user import UserRegister, UserLogin, UserOut
from utils.auth_utils import hash_password, verify_password, create_access_token
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

async def register_user(user: UserRegister, db_session: AsyncSession):
    existing_user = await db_session.scalar(select(User).where(User.username == user.username))
    if existing_user:
        return None
    
    hashed = hash_password(user.password)

    new_user = User(username=user.username, hashed_password=hashed)
    db_session.add(new_user)

    await db_session.commit()

    await db_session.refresh(new_user)

    user_with_books = await db_session.scalar(
        select(User).options(selectinload(User.books)).where(User.id == new_user.id)
    )
    if not user_with_books:
        raise HTTPException(status_code=500, detail="User not found after registration")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(user_with_books).model_dump()}

async def authenticate_user(user: UserLogin, db_session: AsyncSession):
    db_user = await db_session.scalar(
        select(User).options(selectinload(User.books)).where(User.username == user.username)
    )

    if not db_user:
        return None
    if not verify_password(user.password, db_user.hashed_password):
        return None
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer", "user": UserOut.model_validate(db_user).model_dump()}