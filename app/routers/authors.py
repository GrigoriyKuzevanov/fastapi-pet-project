from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import database, models, oauth2, schemas
from app.routers import crud

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get("/", response_model=list[schemas.AuthorOut])
def get_authors(
    limit: int = 10, skip: int = 0, session: Session = Depends(database.get_db)
):
    return crud.read_all_authors(session=session, limit=limit, skip=skip)


@router.get("/{author_id}", response_model=schemas.AuthorOut)
def get_author(author_id: int, session: Session = Depends(database.get_db)):
    db_author = crud.read_author_by_id(session=session, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} does not exist",
        )

    return db_author


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AuthorOut)
def post_author(
    author: schemas.AuthorCreate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    return crud.create_author(session=session, author=author)


@router.put("/{author_id}", response_model=schemas.AuthorOut)
def update_author(
    author_id: int,
    author: schemas.AuthorUpdate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_author = crud.read_author_by_id(session=session, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} does not exist",
        )

    return crud.update_author(session=session, db_author=db_author, update_data=author)


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_author = crud.read_author_by_id(session=session, author_id=author_id)

    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} does not exist",
        )

    crud.delete_author(session=session, author=db_author)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
