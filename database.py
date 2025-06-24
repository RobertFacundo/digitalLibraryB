from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
import os
from dotenv import load_dotenv
import ssl

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if 'localhost' in DATABASE_URL or "127.0.0.1" in DATABASE_URL:

    async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_database_url, echo=True)
else:
    if DATABASE_URL.endswith("?sslmode=require"):
        DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "")
    async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

    ssl_context = ssl.create_default_context()

    engine = create_async_engine(
        async_database_url,
        echo=True,
        connect_args={'ssl': ssl_context}
    )

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)