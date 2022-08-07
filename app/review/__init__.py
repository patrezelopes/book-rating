from sqlalchemy import func
from sqlalchemy.orm import Session
from . import schemas, models


def get_rate_reviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookReview).offset(skip).limit(limit).all()


def _rating_average(db: Session, book_id: str):
    return db.query(func.avg(models.BookReview.rating).label('average')).filter(
        models.BookReview.bookId == book_id).all()


def rating_average(db: Session, book_id: str):
    return _rating_average(db, book_id)


def _get_review_by_book(db: Session, book_id: str):
    return db.query(models.BookReview).filter(models.BookReview.bookId == book_id).all()


def get_review_by_book(db: Session, book_id: str):
    return _get_review_by_book(db, book_id)


def create_review(db: Session, book_id: int, rating: int, review: str, ):
    db_book_review = models.BookReview()
    db_book_review.bookId = book_id
    db_book_review.rating = rating
    db_book_review.review = review
    db.add(db_book_review)
    db.commit()
    db.refresh(db_book_review)
    return db_book_review
