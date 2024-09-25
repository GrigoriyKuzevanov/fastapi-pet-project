from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.core import database
from app.routers import crud

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, session: Session = Depends(database.get_db)):

    if crud.read_user_by_email(session=session, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists!",
        )

    return crud.create_user(session=session, user=user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_users(
    limit: int = 10, skip: int = 0, session: Session = Depends(database.get_db)
):
    return crud.read_all_users(session=session, limit=limit, skip=skip)


@router.get(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def get_user(user_id: int, session: Session = Depends(database.get_db)):
    user = crud.read_user_by_id(session=session, user_id=user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist",
        )

    return user


@router.put("/me", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_user_me(
    user: schemas.UserUpdate,
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    db_user = crud.read_user_by_email(session=session, email=user.email)

    if db_user and db_user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists!",
        )

    return crud.update_user(session=session, db_user=current_user, update_data=user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    session: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    crud.delete_user(session=session, user=current_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    session: Session = Depends(database.get_db),
    current_admin: models.User = Depends(oauth2.get_current_admin),
):
    db_user_by_id = crud.read_user_by_id(session=session, user_id=user_id)

    if not db_user_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist",
        )

    db_user_by_email = crud.read_user_by_email(session=session, email=user.email)

    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists!",
        )

    return crud.update_user(session=session, db_user=db_user_by_id, update_data=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(database.get_db),
    current_admin: models.User = Depends(oauth2.get_current_admin),
):
    db_user = crud.read_user_by_id(session=session, user_id=user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist",
        )

    crud.delete_user(session=session, user=db_user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
