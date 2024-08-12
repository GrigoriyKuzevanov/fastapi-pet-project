from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.routers import crud, dependencies

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
)


@router.get(
    "/", response_model=list[schemas.Author], summary="Get all the authors from the db"
)
async def get_all_authors(session: Session = Depends(dependencies.get_db)):
    db_authors = crud.read_objects(session=session, model_type="author")
    return db_authors


@router.get(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Get the author from the db by given id",
)
async def get_author_by_id(
    author_id: int, session: Session = Depends(dependencies.get_db)
):
    db_author = crud.read_object_by_id(
        session=session, model_type="author", obj_id=author_id
    )
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} is not found",
        )

    return db_author


@router.post(
    "/", response_model=schemas.Author, summary="Create a new author in the db"
)
async def post_author(
    author: schemas.AuthorCreate, session: Session = Depends(dependencies.get_db)
):
    return crud.create_author(session=session, author=author)


@router.put(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Update an author from the db by given id",
)
async def update_author(
    author_id: int,
    author: schemas.AuthorCreate,
    session: Session = Depends(dependencies.get_db),
):
    db_author = crud.update_object_by_id(
        session=session, schema=author, obj_id=author_id, model_type="author"
    )
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} is not found",
        )

    return db_author


@router.patch(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Partically update an author from the db by given id",
)
async def patch_author(
    author_id: int,
    author: schemas.AuthorPartUpdate,
    session: Session = Depends(dependencies.get_db),
):
    db_author = crud.update_object_by_id(
        session=session, schema=author, obj_id=author_id, model_type="author"
    )
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} is not found",
        )

    return db_author


@router.delete(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Delete an author from the db by given id",
)
async def delete_author(
    author_id: int, session: Session = Depends(dependencies.get_db)
):
    db_author = crud.delete_object_by_id(
        session=session, model_type="author", obj_id=author_id
    )
    if db_author is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id: {author_id} is not found",
        )

    return db_author
