from fastapi import FastAPI
from .database import Base, engine
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Knjige Microservice",
    description="Microservice for managing the book catalog.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Knjige microservice is running"}


@app.get("/books")
def get_books():
    return []
