import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.routers.dependencies import get_db

# import random


TEST_SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(
    TEST_SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new db session with a rollback
    at the end of the test.
    """
    connection  = engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Create a test client that uses the override_get_db
    fixture to return a session.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# @pytest.fixture()
# def get_random_id():
#     return random.randint(1, 1000)


@pytest.fixture()
def post_author():
    test_author = {
        "fullname": "Test fullname",
        "first_name": "Test first name",
        "last_name": "Test last name",
        "patronymic": "Test patronymic",
        "birth_date": "1800-01-01",
        "death_date": "1850-12-12",
    }
    return test_author
