from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.lifetime import startup
from app.routers.v1 import review


def create_app(dependency_overrides: dict = {}) -> FastAPI:
    app = FastAPI(
        title="Book Rating API"
    )

    app.include_router(review.router)
    # app.on_event("startup")(startup(app))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.dependency_overrides = dependency_overrides
    return app


app = create_app()
