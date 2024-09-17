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
