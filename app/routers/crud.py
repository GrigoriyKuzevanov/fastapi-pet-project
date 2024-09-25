from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.core.database import Base


# crud functions for books router
def create_book(
    session: Session, book: schemas.BookCreate, owner_id: int
) -> models.Book:
    db_book = models.Book(**book.model_dump(), owner_id=owner_id)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


def read_all_books(session: Session, limit: int, skip: int) -> list:
    stmt = select(models.Book).limit(limit).offset(skip)
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


def read_all_authors(session: Session, limit: int, skip: int) -> list:
    stmt = select(models.Author).limit(limit).offset(skip)
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


def read_all_users(session: Session, limit: int, skip: int) -> list:
    stmt = select(models.User).limit(limit).offset(skip)
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
