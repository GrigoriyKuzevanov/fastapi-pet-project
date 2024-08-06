from datetime import datetime

from pydantic import BaseModel


class BookBase(BaseModel):
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


class AuthorBase(BaseModel):
    fullname: str
    birth_year: datetime
    death_year: datetime | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
