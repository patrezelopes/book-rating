import json
import requests
from functools import lru_cache
from sqlalchemy.orm import Session
from app.settings import settings
from app.review import rating_average, get_review_by_book


class Request:
    url_base = settings.ebook_metadata_url

    def _get(self, path='/'):
        result = requests.get(f'{self.url_base}{path}')
        books = json.loads(result.content)
        return books

    @lru_cache(maxsize=settings.LRU_SIZE)
    def get_books(self, title):
        if title:
            books = self._get(f'?search={title}')
        else:
            books = self._get()
        if books.get('results'):
            response = {'books': books.get('results', [])}
            return response

    @lru_cache(maxsize=settings.LRU_SIZE)
    def get_book(self, id):
        if id:
            books = self._get(f'/{id}')
            response = {'books': books}
            return response


class BookReviewDetail:
    title: str
    authors: list[str]
    languages: list[str]
    rating: float
    reviews: list[str]

    def __init__(self, book: dict, db: Session):
        self.id = book.get('id')
        self.title = book.get('title')
        self.authors = book.get('authors')
        self.languages = book.get('languages')
        self.download_count = book.get('download_count')
        self.rating = rating_average(book_id=self.id, db=db)
        self.reviews = get_review_by_book(book_id=self.id, db=db)
