from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship 
from database import Base

user_books = Table(
    "user_books",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("book_id", String, ForeignKey("books.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    books = relationship("Book", secondary=user_books, back_populates="users")