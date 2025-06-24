from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import auth_controller, library_controller, book_controller
from database import create_db_tables

import models.user
import models.book

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    print("Database tables created (if they didn't exist).")
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router)
app.include_router(library_controller.router)
app.include_router(book_controller.router)

@app.get('/')
def read_root():
    return {"message": 'Welcome to Digital Library Backend'}