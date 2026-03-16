from sqlalchemy.orm import Session
from . import models


def get_all_books(db: Session):
    return db.query(models.Book).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, title: str, author: str, genre: str, available_copies: int):
    book = models.Book(
        title=title,
        author=author,
        genre=genre,
        available_copies=available_copies
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, title: str, author: str, genre: str, available_copies: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None

    book.title = title
    book.author = author
    book.genre = genre
    book.available_copies = available_copies

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None

    db.delete(book)
    db.commit()
    return book
