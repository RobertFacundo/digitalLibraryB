from contextlib import asynccontextmanager
from fastapi import FastAPI
from controllers import auth_controller
from database import database, engine, Base
import models.user

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_controller.router)

@app.get('/')
def read_root():
    return {"message": 'Welcome to Digital Library Backend'}