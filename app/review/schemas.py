from sqlalchemy import Integer, Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.db import Base


class BookReviewBase(Base):
    __tablename__ = "book_review"

    id = Column(Integer, primary_key=True, index=True)
    bookId = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text, nullable=False)
