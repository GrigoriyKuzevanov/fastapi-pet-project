from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import authors, books

# Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(books.router)
app.include_router(authors.router)
