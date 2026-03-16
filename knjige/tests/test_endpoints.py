from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app, get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_books.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_book():
    response = client.post(
        "/books",
        json={
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "genre": "Fantasy",
            "available_copies": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Hobbit"
    assert data["author"] == "J.R.R. Tolkien"


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_book_by_id():
    create_response = client.post(
        "/books",
        json={
            "title": "1984",
            "author": "George Orwell",
            "genre": "Dystopian",
            "available_copies": 5
        }
    )
    book_id = create_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "1984"


def test_update_book():
    create_response = client.post(
        "/books",
        json={
            "title": "Old Title",
            "author": "Author",
            "genre": "Drama",
            "available_copies": 2
        }
    )
    book_id = create_response.json()["id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "New Title",
            "author": "Author Updated",
            "genre": "Drama",
            "available_copies": 4
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["available_copies"] == 4


def test_delete_book():
    create_response = client.post(
        "/books",
        json={
            "title": "Delete Me",
            "author": "Unknown",
            "genre": "Test",
            "available_copies": 1
        }
    )
    book_id = create_response.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
