from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.routers import crud, dependencies

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get(
    "/", response_model=list[schemas.Book], summary="Get all the books from the db"
)
async def get_books(session: Session = Depends(dependencies.get_db)):
    books = crud.read_objects(session=session, db_model_type="book")
    return books


@router.get(
    "/{book_id}",
    response_model=schemas.Book,
    summary="Get the book from the db by given id",
)
async def get_book(book_id: int, session: Session = Depends(dependencies.get_db)):
    db_book = crud.read_object_by_id(
        session=session, obj_id=book_id, db_model_type="book"
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )

    return db_book


@router.put(
    "/{book_id}",
    response_model=schemas.Book,
    summary="Update the book from the db by given id",
)
async def update_book(
    book_id: int,
    book: schemas.BookCreate,
    session: Session = Depends(dependencies.get_db),
):
    db_book = crud.update_book_by_id(session=session, book_id=book_id, book=book)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )

    return db_book


@router.post(
    "/{author_id}",
    response_model=schemas.Book,
    summary="Create a new book in the db by given author id",
)
async def post_book(
    author_id: int,
    book: schemas.BookCreate,
    session: Session = Depends(dependencies.get_db),
):
    return crud.create_book(session=session, book=book, author_id=author_id)


@router.delete(
    "/{book_id}",
    response_model=schemas.Book,
    summary="Delete the book from the db by given id",
)
async def delete_book(book_id: int, session: Session = Depends(dependencies.get_db)):
    db_book = crud.delete_object_by_id(
        session=session, obj_id=book_id, db_model_type="book"
    )
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} is not found",
        )

    return db_book
