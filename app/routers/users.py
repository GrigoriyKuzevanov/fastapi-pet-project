from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import database, models, oauth2, schemas
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
def get_users(session: Session = Depends(database.get_db)):
    return crud.read_all_users(session=session)


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


# @router.put(
#     "/{user_id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut
# )
# def update_user(
#     user_id: int, user: schemas.UserUpdate, session: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)
# ):
#     db_user = crud.read_user_by_id(session=session, user_id=user_id)

#     if not db_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id: {user_id} does not exist",
#         )

#     if db_user.id != current_user.id:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to perfrom requested action"
#         )

#     return crud.update_user(session=session, db_user=db_user, update_data=user)


# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(user_id: int, db: Session = Depends(database.get_db)):
#     user = crud.delete_object_by_id(session=db, model_type="user", obj_id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id: {user_id} is not found",
#         )
