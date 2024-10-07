from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.cache import lifespan
from app.core.config import settings
from app.routers import authors, books, login, users

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    contact={
        "name": settings.contact_name,
        "email": settings.contact_email,
        "url": settings.contact_url,
    },
)


if settings.cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(books.router)
app.include_router(authors.router)
app.include_router(users.router)
app.include_router(login.router)
