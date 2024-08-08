from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fullname: Mapped[str] = mapped_column(String, nullable=False)
    birth_year: Mapped[date] = mapped_column(Date)
    death_year: Mapped[date | None] = mapped_column(Date)

    books: Mapped[list["Book"] | None] = relationship(
        "Book", back_populates="author", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    publish_year: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), nullable=False)

    author: Mapped[Author] = relationship("Author", back_populates="books")
