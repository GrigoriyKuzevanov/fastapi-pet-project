from sqlalchemy.orm import Session

from app import models, schemas


def get_books(db: Session):
    return db.query(models.Book).all()
