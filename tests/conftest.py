from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from app import models
from app.database import SQLALCHEMY_DATABASE_URL, Base, get_db
from app.main import app
from app.oauth2 import create_access_token

TEST_SQLITE_DATABASE_URL = SQLALCHEMY_DATABASE_URL + "_test"


engine = create_engine(TEST_SQLITE_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as testing_session:
        yield testing_session


@pytest.fixture(scope="function")
def client(session: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        with session as s:
            yield s

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client: TestClient) -> dict:
    user_data = {
        "email": "test_user@mail.com",
        "password": "test_secret",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data.get("password")

    return new_user


@pytest.fixture
def test_user2(client: TestClient) -> dict:
    user_data = {
        "email": "test_user2@mail.com",
        "password": "test_secret",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user["password"] = user_data.get("password")

    return new_user


@pytest.fixture
def token(test_user: dict) -> str:
    data = {
        "user_id": test_user.get("id"),
    }
    return create_access_token(data=data)


@pytest.fixture
def authorized_client(client: TestClient, token: str) -> TestClient:
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }

    return client


@pytest.fixture
def test_authors(session: Session) -> list:
    authors_data = [
        {
            "fullname": "test_name1",
            "birth_date": "1901-01-01",
            "death_date": "2000-12-12",
            "description": "test_description1",
        },
        {
            "fullname": "test_name2",
            "birth_date": "1902-02-02",
            "death_date": "2002-11-11",
            "description": "test_description2",
        },
        {
            "fullname": "test_name3",
            "birth_date": "1903-03-03",
            "death_date": "2003-10-10",
            "description": "test_description3",
        },
    ]

    authors_models = [models.Author(**author_data) for author_data in authors_data]

    session.add_all(authors_models)
    session.commit()

    stmt = select(models.Author)
    authors = session.scalars(stmt).all()

    return authors


@pytest.fixture
def test_books(session: Session, test_user: dict, test_authors: list[models.Author]) -> list:
    books_data = [
        {
            "title": "test_title1",
            "genre": "test_genre1",
            "language": "test_language1",
            "publish_date": "1800-01-01",
            "description": "test_description1",
            "author_id": 1,
            "owner_id": test_user.get("id")
        },
        {
            "title": "test_title2",
            "genre": "test_genre2",
            "language": "test_language2",
            "publish_date": "1802-02-02",
            "description": "test_description2",
            "author_id": 2,
            "owner_id": test_user.get("id")
        },
        {
            "title": "test_title3",
            "genre": "test_genre3",
            "language": "test_language3",
            "publish_date": "1803-03-03",
            "description": "test_description3",
            "author_id": 3,
            "owner_id": test_user.get("id")
        },
    ]

    books_models = [models.Book(**book) for book in books_data]
    
    session.add_all(books_models)
    session.commit()
    
    stmt = select(models.Book)
    books = session.scalars(stmt).all()
    
    return books
