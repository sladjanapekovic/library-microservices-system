from fastapi import FastAPI
import httpx

app = FastAPI()

KNJIGE_SERVICE_URL = "http://localhost:8000"
IZPOSOJA_SERVICE_URL = "http://localhost:8082"

# Health check
@app.get("/")
async def root():
    return {"message": "Mobile gateway is running"}

# MOBILE CATALOG - all books
@app.get("/mobile/catalog")
async def get_catalog():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KNJIGE_SERVICE_URL}/books")
        return response.json()

# MOBILE CATALOG - single book
@app.get("/mobile/catalog/{book_id}")
async def get_book(book_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{KNJIGE_SERVICE_URL}/books/{book_id}")
        return response.json()

# USER BORROWINGS
@app.get("/mobile/user-borrowings/{user_id}")
async def get_user_borrowings(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{IZPOSOJA_SERVICE_URL}/borrowings/user/{user_id}")
        return response.json()

# CREATE BORROWING
@app.post("/mobile/borrow")
async def create_borrowing(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{IZPOSOJA_SERVICE_URL}/borrowings", json=data)
        return response.json()
