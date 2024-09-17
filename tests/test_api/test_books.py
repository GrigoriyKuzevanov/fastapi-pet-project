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


@pytest.mark.parametrize(
    "title, genre, language, publish_date, description",
    [
        (
            "test_title1",
            "test_genre1",
            "test_language1",
            "1901-01-12",
            "test_decription1",
        ),
        (
            "test_title2",
            "test_genre2",
            "test_language2",
            "1902-02-11",
            "test_decription2",
        ),
        (
            "test_title3",
            "test_genre3",
            "test_language3",
            "1903-03-10",
            "test_decription3",
        ),
    ],
)
def test_create_book(
    authorized_client: TestClient,
    test_authors: list[models.Author],
    title: str,
    genre: str,
    language: str,
    publish_date: str,
    description: str,
) -> None:
    book_data = {
        "title": title,
        "genre": genre,
        "language": language,
        "publish_date": publish_date,
        "description": description,
        "author_id": 1,
    }
    book_to_post = schemas.BookCreate(**book_data)

    response = authorized_client.post("/books/", json=book_data)

    assert response.status_code == 201

    created_book = schemas.BookOut(**response.json())

    assert created_book.id == 1
    assert created_book.title == book_to_post.title
    assert created_book.genre == book_to_post.genre
    assert created_book.language == book_to_post.language
    assert created_book.publish_date == book_to_post.publish_date
    assert created_book.description == book_to_post.description
    assert created_book.author_id == book_to_post.author_id


def test_create_book_unauthorized(
    client: TestClient, test_authors: list[models.Author]
) -> None:
    book_data = {
        "title": "test_title",
        "genre": "test_genre",
        "language": "test_language",
        "publish_date": "1800-01-01",
        "description": "test_description",
        "author_id": 2,
    }

    response = client.post("/books/", json=book_data)

    assert response.status_code == 401


def test_create_book_author_not_exists(authorized_client: TestClient) -> None:
    author_id = 1111
    book_data = {
        "title": "test_title",
        "genre": "test_genre",
        "language": "test_language",
        "publish_date": "1800-01-01",
        "description": "test_description",
        "author_id": author_id,
    }

    response = authorized_client.post("/books/", json=book_data)

    assert response.status_code == 404
    assert (
        response.json().get("detail") == f"Author with id: {author_id} does not exist"
    )


def test_update_book(
    authorized_client: TestClient, test_books: list[models.Book]
) -> None:
    update_data = {
        "title": "updated_test_title",
        "genre": "updated_test_genre",
        "language": test_books[0].language,
        "publish_date": test_books[0].publish_date.strftime("%Y-%m-%d"),
        "description": "updated_test_title",
    }

    response = authorized_client.put(f"/books/{test_books[0].id}", json=update_data)

    assert response.status_code == 200

    updated_book = schemas.BookOut(**response.json())

    assert updated_book.title == update_data.get("title")
    assert updated_book.genre == update_data.get("genre")
    assert updated_book.language == update_data.get("language")
    assert updated_book.publish_date == test_books[0].publish_date
    assert updated_book.description == update_data.get("description")
    assert updated_book.author_id == test_books[0].author_id


def test_update_book_unauthorized_user(
    client: TestClient, test_books: list[models.Book]
) -> None:
    update_data = {
        "title": "updated_test_title",
        "genre": "updated_test_genre",
        "language": test_books[0].language,
        "publish_date": test_books[0].publish_date.strftime("%Y-%m-%d"),
        "description": "updated_test_title",
    }

    response = client.put(f"/books/{test_books[0].id}", json=update_data)

    assert response.status_code == 401


def test_update_book_not_exists(authorized_client: TestClient) -> None:
    update_data = {
        "title": "updated_test_title",
        "genre": "updated_test_genre",
        "language": "updated_language",
        "publish_date": "1800-01-01",
        "description": "updated_test_title",
    }

    book_id = 1111

    response = authorized_client.put(f"/books/{book_id}", json=update_data)

    assert response.status_code == 404
    assert response.json().get("detail") == f"Book with id: {book_id} does not exist"


def test_delete_book(
    authorized_client: TestClient, test_books: list[models.Book]
) -> None:
    for i in range(1, len(test_books) + 1):
        response = authorized_client.delete(f"/books/{i}")

        assert response.status_code == 204


def test_delete_book_unauthorized_user(
    client: TestClient, test_books: list[models.Book]
) -> None:
    response = client.delete(f"/books/{test_books[0].id}")

    assert response.status_code == 401


def test_delete_book_not_exists(authorized_client: TestClient) -> None:
    book_id = 1111
    response = authorized_client.delete(f"/books/{book_id}")

    assert response.status_code == 404
    assert response.json().get("detail") == f"Book with id: {book_id} does not exist"
