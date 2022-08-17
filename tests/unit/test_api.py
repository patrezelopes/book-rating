import os
from decimal import Decimal
from unittest import mock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.ebook_metadata import Request
from app.settings import settings

client = TestClient(app)
book_request = Request()

@pytest.fixture
def get_book(rf):
    url_books = '/v1/books'
    return rf.get(url_books)


def test_search_by_title():
    with mock.patch("app.services.ebook_metadata.Request._get", return_value={'results': {'id': 1,
                                                                                          'title': 'Blue lagoon'}}):
        result = client.get("/v1/books?title=Blue lagoon")
        response = result.json()
        assert result.status_code == 200
        assert response.get('books').get('id') == 1


def test_book_not_found():
    with mock.patch("app.services.ebook_metadata.Request._get",
                    return_value={"count": 0, "next": None, "previous": None, "results": []}):
        response = client.get("/v1/books?title=book without pages")
        assert response.status_code == 404
        assert response.content == b'{"detail":"Book not found"}'


def test_search_by_title():
    with mock.patch("app.review._rating_average", return_value=[(Decimal('4.5'),)]):
        with mock.patch("app.review._get_review_by_book", return_value={
            "review": "Lorem Ipsum is simply",
            "bookId": 1,
            "rating": 5,
            "id": 1
        }):
            with mock.patch("app.services.ebook_metadata.Request._get",
                            return_value={"id": 11,
                                          'authors': 'Patreze',
                                          'download_count': 1,
                                          'languages': 'en',
                                          "title": "Alice's Adventures in Wonderland"}):
                result = client.get("/v1/books/11")
                response = result.json()
                assert result.status_code == 200
                assert response == {'authors': 'Patreze',
                                    'download_count': 1,
                                    'id': 11,
                                    'languages': 'en',
                                    'rating': [[4.5]],
                                    'reviews': {'bookId': 1,
                                                'id': 1,
                                                'rating': 5,
                                                'review': 'Lorem Ipsum is simply'},
                                    'title': "Alice's Adventures in Wonderland"}


def test_search_by_title_not_found():
    book_request.get_books.cache_clear()
    book_request.get_book.cache_clear()
    with mock.patch("app.services.ebook_metadata.Request._get",
                    return_value={'detail': 'Not found.'}):
        result = client.get("/v1/books/11")
        response = result.json()
        assert result.status_code == 404
        assert response == {'detail': 'Book not found'}
