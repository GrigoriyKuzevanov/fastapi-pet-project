from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Date
from datetime import date


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True)
    fullname: Mapped[str] = mapped_column(String)
    birth_year: Mapped[date] = mapped_column(Date)
    death_year: Mapped[date | None]

    books: Mapped[list["Book"]] = relationship(back_populate="author")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(80), index=True)
    publish_year: Mapped[date] = mapped_column(Date)
    description: Mapped[str | None]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    
    author: Mapped[Author] = relationship(back_poulates="books")
