import json
import asyncio
from sqlalchemy import text
from models.book import Book
from database import AsyncSessionLocal, engine, Base


BOOK_JSON_PATH = 'data/books.json'

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created (if they didn't exist).")

async def load_books_from_json():
    async with AsyncSessionLocal() as db:
        try:

            await db.execute(text("TRUNCATE TABLE books RESTART IDENTITY CASCADE;"))
            print("Existing books purged from database.")

            with open(BOOK_JSON_PATH, 'r', encoding='utf-8') as f:
                books_data = json.load(f)

                books_to_add = []
                for book_data in books_data:
                    book_data['id'] = str(book_data['id'])

                    if 'categories' in book_data and isinstance(book_data['categories'], str):
                        book_data['categories'] = [cat.strip() for cat in book_data['categories'].split(',')]

                    existing_book = await db.get(Book, book_data['id'])

                    new_book = Book(**book_data)
                    books_to_add.append(new_book)

                db.add_all(books_to_add)
                await db.commit()
                print(f"Loaded {len(books_to_add)} books from JSON.")
        except FileNotFoundError:
            print(f"❌ Error: El archivo '{BOOK_JSON_PATH}' no fue encontrado.")
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo '{BOOK_JSON_PATH}' no es un JSON válido.")
        except Exception as e:
            await db.rollback()
            print(f"❌ Ocurrió un error al cargar los libros: {e}")


async def init_db_data():
    await create_db_tables()
    await load_books_from_json()
    
if __name__ == '__main__':
    print("Initializing database data from JSON...")
    asyncio.run(init_db_data())
    print("Database initialization complete.")

        
