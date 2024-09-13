from app import schemas, models
from fastapi.testclient import TestClient


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


def test_get_author_not_exists(client: TestClient) -> None:
    response = client.get("/authors/1")
    
    assert response.status_code == 404
