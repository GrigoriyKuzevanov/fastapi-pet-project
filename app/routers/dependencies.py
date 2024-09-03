from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db


def check_author_exists(
    author: schemas.AuthorCreate, session: Session = Depends(get_db)
):
    stmt = select(models.Author).filter_by(fullname=author.fullname)
    db_author = session.execute(stmt).scalar_one_or_none()

    if db_author:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Author with fullname: {author.fullname} already exists",
        )

    return author
