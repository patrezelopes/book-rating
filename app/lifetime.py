from typing import Awaitable, Callable

from fastapi import FastAPI

from app.db.dependencies import get_db


def startup(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """
    Actions to run on application startup.
    This function use fastAPI app to store data,
    such as db_engine.
    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    async def _startup() -> None:
        app.state.db_reader_engine = get_db()
        app.state.db_writer_engine = get_db()

    return _startup
