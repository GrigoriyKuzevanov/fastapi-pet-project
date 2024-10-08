from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    genre: str
    language: str
    publish_date: date | None = None
    description: str


class BookCreate(BookBase):
    author_id: int


class BookUpdate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    author_id: int
    owner_id: int
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


class AuthorUpdate(AuthorBase):
    pass


class AuthorOut(AuthorBase):
    id: int
    created_at: datetime
    # books: list[BookOut] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
