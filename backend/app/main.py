from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.project_name)
    app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
