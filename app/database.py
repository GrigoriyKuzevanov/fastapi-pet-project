from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName"
SQLALCHEMY_DATABASE_URL = settings.DB_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
