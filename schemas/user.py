from pydantic import BaseModel
from typing import List
from schemas.book import Book

class UserRegister(BaseModel):
    username: str
    password: str
    
class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    books: List[Book] = []

    class Config:
        from_attributes = True