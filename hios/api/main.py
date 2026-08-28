from fastapi import FastAPI

from hios.api.chat import router as chat_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HIOS",
        version="1.0.0",
    )

    app.include_router(
        chat_router
    )

    return app


app = create_app()