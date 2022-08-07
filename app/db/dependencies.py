from app.db import Base
from app.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db():
    db_url = settings.SQLALCHEMY_DATABASE_URL
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    with db:
        yield db
