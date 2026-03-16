from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import repository

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_repository.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_repository_create_and_get_book():
    db = TestingSessionLocal()

    created_book = repository.create_book(
        db,
        title="Clean Code",
        author="Robert C. Martin",
        genre="Programming",
        available_copies=5
    )

    fetched_book = repository.get_book_by_id(db, created_book.id)

    assert fetched_book is not None
    assert fetched_book.title == "Clean Code"
    assert fetched_book.author == "Robert C. Martin"

    db.close()


def test_repository_get_all_books():
    db = TestingSessionLocal()

    repository.create_book(
        db,
        title="Book One",
        author="Author One",
        genre="Fiction",
        available_copies=2
    )

    books = repository.get_all_books(db)

    assert isinstance(books, list)
    assert len(books) >= 1

    db.close()


def test_repository_update_book():
    db = TestingSessionLocal()

    created_book = repository.create_book(
        db,
        title="Old Name",
        author="Old Author",
        genre="Drama",
        available_copies=1
    )

    updated_book = repository.update_book(
        db,
        book_id=created_book.id,
        title="New Name",
        author="New Author",
        genre="Drama",
        available_copies=3
    )

    assert updated_book is not None
    assert updated_book.title == "New Name"
    assert updated_book.available_copies == 3

    db.close()


def test_repository_delete_book():
    db = TestingSessionLocal()

    created_book = repository.create_book(
        db,
        title="Delete Test",
        author="Test Author",
        genre="Test",
        available_copies=1
    )

    deleted_book = repository.delete_book(db, created_book.id)
    fetched_book = repository.get_book_by_id(db, created_book.id)

    assert deleted_book is not None
    assert fetched_book is None

    db.close()
