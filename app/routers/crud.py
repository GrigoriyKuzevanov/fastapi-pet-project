from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# crud functions for books router
def read_books(session: Session):
    stmt = select(models.Book)
    db_books = session.execute(stmt).scalars()
    return db_books


def read_book_by_id(session: Session, book_id: int):
    db_book = session.get(models.Book, book_id)
    return db_book


def create_book(session: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def update_book_by_id(session: Session, book: schemas.BookCreate, book_id: int):
    db_book = session.get(models.Book, book_id)
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


# crud functions for authors router
def read_authors(session: Session):
    stmt = select(models.Author)
    db_authors = session.execute(stmt).scalars()
    return db_authors


def read_author_by_id(session: Session, author_id: int):
    db_author = session.get(models.Author, author_id)
    return db_author


def create_author(session: Session, author: schemas.AuthorCreate):
    new_author = models.Author(**author.model_dump())
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return new_author


def update_author_by_id(session: Session, author: schemas.AuthorCreate, author_id: int):
    db_author = session.get(models.Author, author_id)
    if not db_author:
        return None
    for key, value in author.model_dump().items():
        setattr(db_author, key, value)

    session.commit()
    session.refresh(db_author)
    return db_author


def delete_author_by_id(session: Session, author_id: int):
    db_author = session.get(models.Author, author_id)
    if not db_author:
        return None
    session.delete(db_author)
    session.commit()
    return db_author
