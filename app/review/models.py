from app.review.schemas import BookReviewBase


class BookReview(BookReviewBase):
    id: int
    bookId: int
    rating: int
    review: str

    class Config:
        orm_mode = True
