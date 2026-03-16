from fastapi import FastAPI

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
