from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


def read_books(session: Session):
    stmt = select(models.Book)
    books = session.execute(stmt).scalars()
    return books


def read_book_by_id(session: Session, book_id: int):
    stmt = select(models.Book).where(models.Book.id == book_id)
    result = session.execute(stmt).scalar_one_or_none()
    return result


def create_book(session: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def update_book_by_id(session: Session, book: schemas.BookCreate, book_id: int):
    stmt = select(models.Book).filter_by(id=book_id)
    db_book = session.execute(stmt).scalar_one_or_none()
    if not db_book:
        return None
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    session.commit()
    session.refresh(db_book)
    return db_book


def delete_book_by_id(session: Session, book_id: int):
    db_book = session.get(models.Book, book_id)
    if not db_book:
        return None
    session.delete(db_book)
    session.commit()
    return db_book
