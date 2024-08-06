from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.routers import crud
from app import models, schemas
from app.database import SessionLocal

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

# TODO relocate to dependencies.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Book])
async def read_books(db: Session = Depends(get_db)):
    books = crud.get_books(db=db)
    return books


@router.post("/")
async def post_books():
    return {"books": "post book"}
