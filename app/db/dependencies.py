from asyncio import current_task
from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import configure_mappers, sessionmaker

from app.db import SessionLocal
from app.settings import settings


def get_db():
    db = SessionLocal()
    with db:
        yield db
