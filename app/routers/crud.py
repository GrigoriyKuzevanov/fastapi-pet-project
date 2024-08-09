from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base

DB_MODEL_CHOICES = {
    "book": models.Book,
    "author": models.Author,
}


# mutual crud functions for routers
def read_objects(session: Session, db_model_type: str):
    stmt = select(DB_MODEL_CHOICES[db_model_type])
    db_objects = session.execute(stmt).scalars()
    return db_objects


def read_object_by_id(session: Session, db_model_type: str, obj_id: int):
    db_object = session.get(DB_MODEL_CHOICES[db_model_type], obj_id)
    return db_object


def delete_object_by_id(session: Session, db_model_type: str, obj_id: int):
    db_object = session.get(DB_MODEL_CHOICES[db_model_type], obj_id)
    if not db_object:
        return None
    session.delete(db_object)
    session.commit()
    return db_object


# crud functions for books router
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


# crud functions for authors router
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
