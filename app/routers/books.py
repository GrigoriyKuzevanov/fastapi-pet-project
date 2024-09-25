from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.core import database
from app.routers import crud

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.get("/", response_model=list[schemas.BookOut])
def get_books(
    limit: int = 10, skip: int = 0, session: Session = Depends(database.get_db)
):
    return crud.read_all_books(session=session, limit=limit, skip=skip)


@router.get("/{book_id}", response_model=schemas.BookOut)
def get_book(book_id: int, session: Session = Depends(database.get_db)):
    db_book = crud.read_book_by_id(session=session, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} does not exist",
        )

    return db_book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_book = crud.read_book_by_id(session=session, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} does not exist",
        )

    if db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perfrom requested action",
        )

    return crud.update_book(session=session, db_book=db_book, update_data=book)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BookOut)
def post_book(
    book: schemas.BookCreate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # check author exists
    db_author = crud.read_author_by_id(session=session, author_id=book.author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {book.author_id} does not exist",
        )

    db_book = crud.create_book(session=session, book=book, owner_id=current_user.id)

    return db_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_book = crud.read_book_by_id(session=session, book_id=book_id)

    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} does not exist",
        )

    if db_book.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perfrom requested action",
        )

    crud.delete_book(session=session, book=db_book)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
