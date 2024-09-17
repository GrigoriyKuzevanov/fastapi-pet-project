import datetime

import pytest
from fastapi.testclient import TestClient

from app import models, schemas
from tests.utils import users_utils


def test_get_users(client: TestClient, test_user: dict) -> None:
    response = client.get("/users/")

    assert response.status_code == 200

    users = [schemas.UserOut(**user) for user in response.json()]

    assert len(users) == 1

    for user in users:
        assert user.id == test_user.get("id")
        assert user.email == test_user.get("email")
        assert user.created_at == users_utils.string_to_datetime(
            test_user.get("created_at")
        )


def test_get_user(client: TestClient, test_user: dict) -> None:
    response = client.get(f"/users/{test_user.get("id")}")

    assert response.status_code == 200

    user = schemas.UserOut(**response.json())

    assert user.id == test_user.get("id")
    assert user.email == test_user.get("email")
    assert user.created_at == users_utils.string_to_datetime(
        test_user.get("created_at")
    )


@pytest.mark.parametrize(
    "password, email",
    [
        ("test_password1", "test_email1@email.com"),
        ("test_password2", "test_email2@mail.com"),
        ("test_password3", "test_email3@mail.com"),
    ],
)
def test_create_user(client: TestClient, password: str, email: str) -> None:
    user_data = {
        "password": password,
        "email": email,
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    user = schemas.UserOut(**response.json())

    assert user.email == user_data.get("email")


def test_create_user_email_exists(client: TestClient, test_user: dict) -> None:
    existing_email = test_user.get("email")
    user_data = {
        "password": "secret",
        "email": existing_email,
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == 409
    assert (
        response.json().get("detail")
        == f"User with email: {existing_email} already exists!"
    )
