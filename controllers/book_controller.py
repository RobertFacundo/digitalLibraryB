from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_async_db

from schemas.book import Book
from models.book import Book as BookModel


router = APIRouter(prefix='/books', tags=["books"])


@router.get("/", response_model=list[Book])
async def get_all_books(db_session: AsyncSession = Depends(get_async_db)):
    
    result = await db_session.execute(select(BookModel))
    books = result.scalars().all()
    return books