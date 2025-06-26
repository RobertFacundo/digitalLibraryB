import json
import asyncio
from sqlalchemy import text, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import Book
from database import AsyncSessionLocal, engine, Base, get_async_db


BOOK_JSON_PATH = 'data/books.json'

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (if they didn't exist).")

async def load_books_from_json_conditionally(db_session: AsyncSession):

    existing_books_count = await db_session.scalar(select(func.count()).select_from(Book))

    if existing_books_count > 0:
        print(f"Database already contains {existing_books_count} books. Skipping initial book loading.")
        return
    
    print("Database 'books' table is empty. Attempting to load books from JSON...")

    try:
        with open(BOOK_JSON_PATH, 'r', encoding='utf-8') as f:
            books_data = json.load(f)
        books_to_add = []
        for book_data in books_data:
            book_data['id'] = str(book_data['id'])

            if 'categories' in book_data and isinstance(book_data['categories'], str):
                book_data['categories'] = [cat.strip() for cat in book_data['categories'].split(',')]
            books_to_add.append(Book(**book_data))

        db_session.add_all(books_to_add)
        await db_session.commit()
        print(f"Successfully loaded {len(books_to_add)} books from JSON into the database.")
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{BOOK_JSON_PATH}' no fue encontrado.")
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo '{BOOK_JSON_PATH}' no es un JSON válido.")
    except Exception as e:
        await db.rollback()
        print(f"❌ Ocurrió un error al cargar los libros: {e}")
    else:
        pass

    
if __name__ == '__main__':
    print("Initializing database data from JSON...")
    async def _run_seed_test():
        await create_db_tables()
        async for session in get_async_db(): # Usa get_async_db para obtener la sesión
            await load_books_from_json_conditionally(session)
            break
    asyncio.run(_run_seed_test())
    print("Database initialization complete (via script).")

        
