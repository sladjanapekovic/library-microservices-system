import logging

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal, wait_for_database
from . import schemas, repository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

wait_for_database()
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
    return repository.get_all_books(db)


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching book with id={book_id}")
    book = repository.get_book_by_id(db, book_id)

    if not book:
        logger.warning(f"Book with id={book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating book with title={book.title}")

    return repository.create_book(
        db,
        book.title,
        book.author,
        book.genre,
        book.available_copies
    )


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
    logger.info(f"Updating book with id={book_id}")

    book = repository.update_book(
        db,
        book_id,
        updated_book.title,
        updated_book.author,
        updated_book.genre,
        updated_book.available_copies
    )

    if not book:
        logger.warning(f"Book with id={book_id} not found for update")
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting book with id={book_id}")

    book = repository.delete_book(db, book_id)

    if not book:
        logger.warning(f"Book with id={book_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}
