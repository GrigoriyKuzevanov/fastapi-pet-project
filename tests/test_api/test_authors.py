import pytest
from fastapi.testclient import TestClient

from app import models, schemas


def test_get_authors(client: TestClient, test_authors: list[models.Author]) -> None:
    response = client.get("/authors/")
    
    assert response.status_code == 200
    
    authors = [schemas.AuthorOut(**author) for author in response.json()]

    assert len(authors) == len(test_authors)

    for index, author in enumerate(authors):
        assert author.fullname == test_authors[index].fullname
        assert author.birth_date == test_authors[index].birth_date
        assert author.death_date == test_authors[index].death_date
        assert author.description == test_authors[index].description

    


@pytest.mark.parametrize("author_id", [1, 2, 3])
def test_get_author(
    client: TestClient, test_authors: list[models.Author], author_id: int
) -> None:
    response = client.get(f"/authors/{author_id}")
    
    assert response.status_code == 200
    
    author = schemas.AuthorOut(**response.json())

    assert author.fullname == test_authors[author_id - 1].fullname
    assert author.birth_date == test_authors[author_id - 1].birth_date
    assert author.death_date == test_authors[author_id - 1].death_date
    assert author.description == test_authors[author_id - 1].description


def test_get_author_not_exists(client: TestClient) -> None:
    response = client.get("/authors/1")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "fullname, birth_date, death_date, description",
    [
        (
            "test_post_author_1",
            "1799-06-06",
            "1837-02-10",
            "test_post_author_description_1",
        ),
        (
            "test_post_author_2",
            "1600-01-12",
            "1670-11-11",
            "test_post_author_description_2",
        ),
        (
            "test_post_author_3",
            "1800-07-07",
            "1900-10-10",
            "test_post_author_description_3",
        ),
    ],
)
def test_post_author(
    authorized_client: TestClient,
    fullname: str,
    birth_date: str,
    death_date: str,
    description: str,
) -> None:
    author_data = {
        "fullname": fullname,
        "birth_date": birth_date,
        "death_date": death_date,
        "description": description,
    }
    author_to_post = schemas.AuthorCreate(**author_data)

    response = authorized_client.post("/authors/", json=author_data)

    assert response.status_code == 201

    created_author = schemas.AuthorOut(**response.json())

    assert created_author.id == 1
    assert created_author.fullname == author_to_post.fullname
    assert created_author.birth_date == author_to_post.birth_date
    assert created_author.death_date == author_to_post.death_date
    assert created_author.description == author_to_post.description


def test_post_author_unauthorized_user(client: TestClient):
    author_data = {
        "fullname": "test_fullname",
        "birth_date": "test_birth_date",
        "death_date": "test_death_date",
        "description": "test_description",
    }

    response = client.post("/authors/", json=author_data)

    assert response.status_code == 401


def test_update_author(
    authorized_client: TestClient, test_authors: list[models.Author]
) -> None:
    update_data = {
        "fullname": "updated_test_fullname",
        "birth_date": test_authors[0].birth_date.strftime("%Y-%m-%d"),
        "death_date": test_authors[0].death_date.strftime("%Y-%m-%d"),
        "description": test_authors[0].description,
    }

    response = authorized_client.put(f"/authors/{test_authors[0].id}", json=update_data)

    assert response.status_code == 200

    updated_author = schemas.AuthorOut(**response.json())

    assert updated_author.fullname == update_data.get("fullname")
    assert updated_author.birth_date == test_authors[0].birth_date
    assert updated_author.death_date == test_authors[0].death_date
    assert updated_author.description == test_authors[0].description
    assert updated_author.id == test_authors[0].id


def test_update_author_unauthorized_user(
    client: TestClient, test_authors: list[models.Author]
) -> None:
    update_data = {
        "fullname": "updated_test_fullname",
        "birth_date": "1500-01-02",
        "death_date": "1550-02-01",
        "description": test_authors[0].description,
    }

    response = client.put(f"/authors/{test_authors[0].id}", json=update_data)

    assert response.status_code == 401


def test_update_author_not_exists(authorized_client: TestClient) -> None:
    update_data = {
        "fullname": "updated_test_fullname",
        "birth_date": "1500-01-02",
        "death_date": "1550-02-01",
        "description": "updated_test_description",
    }
    author_id = 1111
    response = authorized_client.put(f"/authors/{author_id}", json=update_data)

    assert response.status_code == 404
    assert (
        response.json().get("detail") == f"Author with id: {author_id} does not exist"
    )


def test_delete_author(
    authorized_client: TestClient, test_authors: list[models.Author]
) -> None:
    for i in range(1, len(test_authors) + 1):
        response = authorized_client.delete(f"/authors/{i}")

        assert response.status_code == 204


def test_delete_author_unauthorized_user(
    client: TestClient, test_authors: list[models.Author]
) -> None:
    response = client.delete("/authors/1")

    assert response.status_code == 401


def test_delete_author_not_exists(authorized_client: TestClient) -> None:
    author_id = 1111
    response = authorized_client.delete(f"/authors/{author_id}")

    assert response.status_code == 404
    assert (
        response.json().get("detail") == f"Author with id: {author_id} does not exist"
    )
