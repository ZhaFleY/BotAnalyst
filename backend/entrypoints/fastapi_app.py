from fastapi import FastAPI

from backend.infrastructure.s3 import init_bucket
from backend.presentation.api.routers import file_router


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(file_router.router)

    @app.on_event("startup")
    def startup():
        init_bucket()

    @app.get("/")
    def main():
        return {"message": "I'm Alive"}

    return app


app = create_app()

