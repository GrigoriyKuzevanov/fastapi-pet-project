from datetime import date, datetime

from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    genre: str
    language: str
    publish_date: date | None = None
    description: str
    author_id: int


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AuthorBase(BaseModel):
    fullname: str
    birth_date: date | None = None
    death_date: date | None = None
    description: str


class AuthorCreate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    id: int
    created_at: datetime
    books: list[BookOut] = []

    class Config:
        from_attributes = True
