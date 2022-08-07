from typing import Any, Tuple
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import as_declarative

from app.settings import settings

meta_data = MetaData()


@as_declarative(metadata=meta_data)
class Base:
    """
    Base for all models.

    It has some type definitions to
    enhance autocompletion.
    """

    __tablename__: str
    __table__: Table
    __table_args__: Tuple[Any, ...]


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = settings.SQLALCHEMY_DATABASE_URL
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
meta_data.create_all(bind=engine)
