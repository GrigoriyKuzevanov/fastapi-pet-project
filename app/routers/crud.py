from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base

DB_MODEL_CHOICES = {
    "book": models.Book,
    "author": models.Author,
}


# mutual crud functions for routers
def read_objects(session: Session, model_type: str):
    stmt = select(DB_MODEL_CHOICES[model_type])
    db_objects = session.execute(stmt).scalars()
    return db_objects


def read_object_by_id(session: Session, model_type: str, obj_id: int):
    db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
    return db_object


def delete_object_by_id(session: Session, model_type: str, obj_id: int):
    db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
    if not db_object:
        return None
    session.delete(db_object)
    session.commit()
    return db_object


def update_object_by_id(
    session: Session, schema: schemas.BookCreate, obj_id: int, model_type: str
):
    db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
    if not db_object:
        return None
    for key, value in schema.model_dump().items():
        setattr(db_object, key, value)
    session.commit()
    session.refresh(db_object)
    return db_object


# crud functions for books router
# TODO добавить проверку: author с переданным auhtor_id существует в таблице
def create_book(session: Session, book: schemas.BookCreate, author_id: int):
    db_author = session.get(models.Author, author_id)
    if not db_author:
        return None
    db_book = models.Book(**book.model_dump(), author_id=author_id)
    session.add(db_book)
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
