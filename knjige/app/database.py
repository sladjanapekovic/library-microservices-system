import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./books.db")

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def wait_for_database(retries=10, delay=3):
    for attempt in range(retries):
        try:
            connection = engine.connect()
            connection.close()
            print("Database connection successful.")
            return
        except OperationalError:
            print(f"Database not ready yet. Retrying in {delay} seconds...")
            time.sleep(delay)

    raise Exception("Database connection failed after multiple retries.")
