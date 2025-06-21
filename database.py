from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base()
