from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import Base

# DB_MODEL_CHOICES = {
#     "book": models.Book,
#     "author": models.Author,
#     "user": models.User,
# }


# # mutual crud functions for routers
# def read_objects(session: Session, model_type: str):
#     stmt = select(DB_MODEL_CHOICES[model_type])
#     db_objects = session.execute(stmt).scalars().all()
#     return db_objects


# def read_object_by_id(session: Session, model_type: str, obj_id: int):
#     db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
#     print(type(db_object.__class__))
#     return db_object


# def delete_object_by_id(session: Session, model_type: str, obj_id: int):
#     db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
#     if not db_object:
#         return None
#     session.delete(db_object)
#     session.commit()
#     return db_object


# def update_object_by_id(
#     session: Session, schema: schemas.BaseModel, obj_id: int, model_type: str
# ):
#     db_object = session.get(DB_MODEL_CHOICES[model_type], obj_id)
#     if not db_object:
#         return None
#     for key, value in schema.model_dump(exclude_unset=True).items():
#         setattr(db_object, key, value)
#     session.commit()
#     session.refresh(db_object)
#     return db_object


# crud functions for books router
def create_book(
    session: Session, book: schemas.BookCreate, owner_id: int
) -> models.Book:
    db_book = models.Book(**book.model_dump(), owner_id=owner_id)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


def read_all_books(session: Session) -> list:
    stmt = select(models.Book)
    db_books = session.scalars(stmt).all()

    return db_books


def read_book_by_id(session: Session, book_id: int) -> models.Book | None:
    return session.get(models.Book, book_id)


def update_book(
    session: Session, db_book: models.Book, update_data: schemas.BookUpdate
) -> models.Book:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    session.commit()
    session.refresh(db_book)

    return db_book


def delete_book(session: Session, book: models.Book) -> None:
    session.delete(book)
    session.commit()


# crud functions for authors router
def create_author(session: Session, author: schemas.AuthorCreate) -> models.Author:
    db_author = models.Author(**author.model_dump())
    session.add(db_author)
    session.commit()
    session.refresh(db_author)

    return db_author


def read_all_authors(session: Session) -> list:
    stmt = select(models.Author)
    db_authors = session.scalars(stmt).all()

    return db_authors


def read_author_by_id(session: Session, author_id: int) -> models.Author | None:
    return session.get(models.Author, author_id)


def update_author(
    session: Session, db_author: models.Author, update_data: schemas.AuthorUpdate
) -> models.Author:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_author, key, value)
    session.commit()
    session.refresh(db_author)

    return db_author


def delete_author(session: Session, author: models.Author) -> None:
    session.delete(author)
    session.commit()


# crud functions for users router
def create_user(session: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def read_user_by_email(session: Session, email: str) -> models.User | None:
    stmt = select(models.User).where(models.User.email == email)
    db_user = session.execute(stmt).scalar_one_or_none()

    return db_user


def read_all_users(session: Session) -> list:
    stmt = select(models.User)
    db_users = session.scalars(stmt).all()

    return db_users


def read_user_by_id(session: Session, user_id: int) -> models.User | None:
    return session.get(models.User, user_id)


def update_user(
    session: Session, db_user: models.User, update_data: schemas.UserUpdate
) -> models.User:
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)

    return db_user


def delete_user(session: Session, user: models.User) -> None:
    session.delete(user)
    session.commit()
