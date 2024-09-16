import pytest
from fastapi.testclient import TestClient

from app import models, schemas


def test_get_books(client: TestClient, test_books: list[models.Book]) -> None:
    response = client.get("/books/")

    assert response.status_code == 200

    books = [schemas.BookOut(**book) for book in response.json()]

    assert len(books) == len(test_books)

    for index, book in enumerate(books):
        assert book.title == test_books[index].title
        assert book.genre == test_books[index].genre
        assert book.language == test_books[index].language
        assert book.publish_date == test_books[index].publish_date
        assert book.description == test_books[index].description
        assert book.author_id == test_books[index].author_id
        assert book.owner_id == test_books[index].owner_id


@pytest.mark.parametrize("book_id", [1, 2, 3])
def test_get_book(
    client: TestClient, test_books: list[models.Book], book_id: int
) -> None:
    response = client.get(f"/books/{book_id}")

    assert response.status_code == 200

    book = schemas.BookOut(**response.json())

    assert book.title == test_books[book_id - 1].title
    assert book.genre == test_books[book_id - 1].genre
    assert book.language == test_books[book_id - 1].language
    assert book.description == test_books[book_id - 1].description
    assert book.author_id == test_books[book_id - 1].author_id
    assert book.owner_id == test_books[book_id - 1].owner_id
