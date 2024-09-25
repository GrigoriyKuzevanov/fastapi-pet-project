import logging

from sqlalchemy.orm import Session

from app import models, utils
from app.core.config import settings
from app.core.database import SessionLocal
from app.routers import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_first_admin(session: Session) -> None:
    try:
        db_user = crud.read_user_by_email(session=session, email=settings.admin_email)
        if not db_user:
            hashed_password = utils.hash(settings.admin_password)

            admin_data = {
                "email": settings.admin_email,
                "password": hashed_password,
                "is_admin": True,
            }

            admin = models.User(**admin_data)

            session.add(admin)
            session.commit()

            logger.info(f"Admin is created")
            
        else:
            logger.info(f"User with email: {settings.admin_email} already exists!")
            
    except Exception as error:
        logger.error(f"Error while creating admin: {error}")


if __name__ == "__main__":
    with SessionLocal() as session:
        create_first_admin(session=session)
