import logging

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Knjige Microservice",
    description="Microservice for managing the book catalog.",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Knjige microservice is running"}


@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    logger.info("Fetching all books")
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching book with id={book_id}")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        logger.warning(f"Book with id={book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating book with title='{book.title}'")
    db_book = models.Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        available_copies=book.available_copies
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    logger.info(f"Book created with id={db_book.id}")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating book with id={book_id}")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        logger.warning(f"Book with id={book_id} not found for update")
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    book.genre = updated_book.genre
    book.available_copies = updated_book.available_copies

    db.commit()
    db.refresh(book)
    logger.info(f"Book with id={book_id} updated successfully")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting book with id={book_id}")
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        logger.warning(f"Book with id={book_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    logger.info(f"Book with id={book_id} deleted successfully")
    return {"message": "Book deleted successfully"}
