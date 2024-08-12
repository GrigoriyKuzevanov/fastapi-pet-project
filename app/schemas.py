from datetime import date

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    genre: str
    language: str
    publish_date: date
    description: str | None = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    fullname: str
    first_name: str
    last_name: str
    patronymic: str | None = None
    birth_date: date
    death_date: date | None = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    # books: list[Book] = []

    class Config:
        from_attributes = True
