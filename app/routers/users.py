from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.routers import crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(session=db, user=user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    return crud.read_objects(session=db, model_type="user")


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.read_object_by_id(session=db, model_type="user", obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} is not found",
        )

    return user


# TODO добавить обработку ограничений на уникальные username и email
@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)
):
    user = crud.update_object_by_id(
        session=db, schema=user, obj_id=user_id, model_type="user"
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} is not found",
        )

    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = crud.delete_object_by_id(session=db, model_type="user", obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} is not found",
        )
