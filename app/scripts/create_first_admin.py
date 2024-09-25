from sqlalchemy.orm import Session

from app import models, utils
from app.core.config import settings
from app.core.database import SessionLocal


def create_first_admin(session: Session) -> None:
    hashed_password = utils.hash(settings.admin_password)

    admin_data = {
        "email": settings.admin_email,
        "password": hashed_password,
        "is_admin": True,
    }

    admin = models.User(**admin_data)

    session.add(admin)
    session.commit()


if __name__ == "__main__":
    with SessionLocal() as session:
        create_first_admin(session=session)
