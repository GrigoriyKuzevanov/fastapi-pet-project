from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, models, oauth2, schemas
from app.routers import crud

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get(
    "/", response_model=list[schemas.BookOut], summary="Get all the books from the db"
)
def get_books(session: Session = Depends(database.get_db)):
    books = crud.read_objects(session=session, model_type="book")
    return books


@router.get(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Get the book from the db by given id",
)
def get_book(book_id: int, session: Session = Depends(database.get_db)):
    db_book = crud.read_object_by_id(session=session, obj_id=book_id, model_type="book")
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )

    return db_book


@router.put(
    "/{book_id}",
    response_model=schemas.BookOut,
    summary="Update the book from the db by given id",
)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    session: Session = Depends(database.get_db),
):
    db_book = crud.update_object_by_id(
        session=session, schema=book, obj_id=book_id, model_type="book"
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )

    return db_book


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BookOut,
    summary="Create a new book in the db by given author id",
)
def post_book(
    book: schemas.BookCreate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # check author exists
    db_author = session.get(models.Author, book.author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {book.author_id} is not found",
        )

    db_book = crud.create_book(session=session, book=book, owner_id=current_user.id)

    return db_book


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete the book from the db by given id",
)
def delete_book(book_id: int, session: Session = Depends(database.get_db)):
    db_book = crud.delete_object_by_id(
        session=session, obj_id=book_id, model_type="book"
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )
