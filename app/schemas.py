from pydantic import BaseModel
from datetime import datetime


class BookBase(BaseModel):
    author: str
    title: str
    publish_year: datetime
    description: str | None = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True
