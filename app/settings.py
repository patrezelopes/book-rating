from pydantic import BaseSettings, AnyHttpUrl
from sqlalchemy.engine import make_url, URL


class Settings(BaseSettings):
    """Application settings."""

    service_name: str = "book-rating-api"
    ebook_metadata_url: AnyHttpUrl = "https://gutendex.com/books"
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:postgres@localhost/book_db"
    LRU_SIZE: int = 32

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
