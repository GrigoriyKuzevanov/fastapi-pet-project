from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# postgres://YourUserName:YourPassword@YourHostname:5432/YourDatabaseName"
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocmmit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
