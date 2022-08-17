from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.db.dependencies import get_db
from app.main import app
from tests.unit.test_api import book_request

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_post_review():
    book_request.get_books.cache_clear()
    book_request.get_book.cache_clear()
    result = client.post("v1/books/review",
                         json={
                             "bookId": 11,
                             "rating": 4,
                             "review": "Lorem Ipsum is simply"
                         }
                         )
    response = result.json()
    response.pop('id')
    assert result.status_code == 200
    assert response == {'rating': 4, 'review': 'Lorem Ipsum is simply', 'bookId': 11}
