from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db

from auth.dependencies import get_current_user

from models.user import User
from services import library_service
from schemas.book import Book

router = APIRouter(prefix="/library", tags=["library"])

@router.post("/", response_model=Book)
async def add_book(
    book_id: str, 
    current_user: User = Depends(get_current_user), 
    db_session: AsyncSession = Depends(get_async_db)
    ):
    return await library_service.add_book_to_library(current_user.id, book_id, db_session)

@router.get("/", response_model=list[Book])
async def get_library(
    current_user: User = Depends(get_current_user), 
    db_session: AsyncSession = Depends(get_async_db)
    ):
    return await library_service.get_user_library(current_user.id, db_session)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: str, 
    current_user: User = Depends(get_current_user), 
    db_session: AsyncSession = Depends(get_async_db)
    ):
    return await library_service.remove_book_from_library(current_user.id, book_id, db_session)