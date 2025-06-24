from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db

from models.user import User

from utils.auth_utils import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
        token: str=Depends(oauth2_scheme),
        db_session: AsyncSession = Depends(get_async_db)
) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    username = decode_access_token(token)
    if username is None:
        raise credentials_exception
    
    user = await db_session.scalar(select(User).where(User.username == username))

    if user is None:
        raise credentials_exception
    
    return user