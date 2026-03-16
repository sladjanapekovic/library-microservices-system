from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from . import models, schemas

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
    return {"message": "Knjige microservice is running"}


@app.get("/books", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        available_copies=book.available_copies
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
