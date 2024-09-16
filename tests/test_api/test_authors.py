import pytest
from fastapi.testclient import TestClient

from app import models, schemas


def test_get_authors(client: TestClient, test_authors: list[models.Author]) -> None:
    response = client.get("/authors/")
    authors = [schemas.AuthorOut(**author) for author in response.json()]

    assert len(authors) == len(test_authors)

    for index, author in enumerate(authors):
        assert author.fullname == test_authors[index].fullname
        assert author.birth_date == test_authors[index].birth_date
        assert author.death_date == test_authors[index].death_date
        assert author.description == test_authors[index].description

    assert response.status_code == 200


@pytest.mark.parametrize("author_id", [1, 2, 3])
def test_get_author(
    client: TestClient, test_authors: list[models.Author], author_id: int
) -> None:
    response = client.get(f"/authors/{author_id}")
    author = schemas.AuthorOut(**response.json())

    assert response.status_code == 200

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
