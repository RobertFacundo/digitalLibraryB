from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int]
    synopsis: Optional[str] = None
    coverImageUrl: Optional[str] = None
    categories: List[str]

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: str

    class Config:
        from_attributes = True