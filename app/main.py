from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import authors, books, login, users

# Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(login.router)
