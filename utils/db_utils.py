import json
import asyncio
from models.book import Book
from database import AsyncSessionLocal

async def load_books_from_json(json_file: str):
    async with AsyncSessionLocal() as db:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                books_data = json.load(f)
                for book_data in books_data:
                    book_data['id'] = str(book_data['id'])

                    if 'categories' in book_data and isinstance(book_data['categories'], str):
                        book_data['categories'] = [cat.strip() for cat in book_data['categories'].split(',')]

                    existing_book = await db.get(Book, book_data['id'])

                    if existing_book:
                        for key, value in book_data.items():
                            setattr(existing_book, key, value)
                        print(f"🔄 Libro actualizado: {existing_book.title}")
                    else:
                        book = Book(**book_data)
                        db.add(book)
                        print(f"➕ Libro agregado: {book.title}")
                await db.commit()
                print(f"✅ Libros cargados exitosamente desde '{json_file}' en la base de datos.")
        except FileNotFoundError:
            print(f"❌ Error: El archivo '{json_file}' no fue encontrado.")
        except json.JSONDecodeError:
            print(f"❌ Error: El archivo '{json_file}' no es un JSON válido.")
        except Exception as e:
            await db.rollback()
            print(f"❌ Ocurrió un error al cargar los libros: {e}")
    
if __name__ == '__main__':

    asyncio.run(load_books_from_json('data/books.json'))

        
