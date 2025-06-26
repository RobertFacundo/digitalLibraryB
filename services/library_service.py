from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.user import User
from models.book import Book
from sqlalchemy.orm import selectinload

async def add_book_to_library(user_id: int, book_id: str, db_session: AsyncSession):
    user_query = await db_session.execute(
        select(User).options(selectinload(User.books)).where((User.id == user_id))
    )
    user = user_query.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    
    book = await db_session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    
    
    if book in user.books:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Book already in library')
    
    user.books.append(book)
    await db_session.commit()


    await db_session.refresh(user)
    await db_session.refresh(user, attribute_names=["books"])

    return user

async def get_user_library(user_id: int, db_session: AsyncSession):
    user = await db_session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db_session.refresh(user, attribute_names=["books"])
    return user.books

async def remove_book_from_library(user_id: int, book_id: str, db_session: AsyncSession):
    user_query = await db_session.execute(
        select(User).options(selectinload(User.books)).where(User.id == user_id)
    )
    user = user_query.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    book = await db_session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    
    if book not in user.books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found in library")
    
    user.books.remove(book)
    await db_session.commit()

    await db_session.refresh(user)
    await db_session.refresh(user, attribute_names=["books"])
    
    return user