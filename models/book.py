from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base
from models.user import user_books
from sqlalchemy.dialects.postgresql import ARRAY

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    synopsis = Column(String)
    coverImageUrl = Column(String)
    categories = Column(ARRAY(String))

    users = relationship("User", secondary=user_books, back_populates="books")