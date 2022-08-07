import json

from fastapi import APIRouter, Path, Body, Query
from starlette.responses import Response

from app.db.dependencies import get_db
from app.review import create_review, get_review_by_book, rating_average
from app.services.ebook_metadata import Request
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.review.schemas import BookReviewBase
from app.services.ebook_metadata import BookReviewDetail

router = APIRouter(
    prefix="/v1/books",
    tags=["v1"]
)

request = Request()


@router.get("/")
def get_books(title: str = None):
    books = request.get_books(title=title)
    if books:
        return Response(json.dumps(books))
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@router.post("/review")
def post_review(bookId: int = Body(ge=1, embed=True), rating: int = Body(ge=1, le=5, embed=True),
                review: str = Body(embed=True), db: Session = Depends(get_db)):
    try:
        book = request.get_book(id=bookId).get('books')
    except Exception:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.get('id'):
        rating_review = create_review(db=db, book_id=bookId, rating=rating, review=review)
        return rating_review
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@router.get("/{bookId}")
def get_book_detail(bookId: int = Path(title="Reviews for book"), db: Session = Depends(get_db)):
    try:
        book = request.get_book(id=bookId).get('books')
    except Exception:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        if book.get('id'):
            rating_review = BookReviewDetail(book=book, db=db)
            return rating_review
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except (Exception,):
        raise HTTPException(status_code=404, detail="Book not found")
