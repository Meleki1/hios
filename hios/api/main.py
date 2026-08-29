from fastapi import FastAPI

from hios.api.chat import router as chat_router
from hios.api.telegram import router as telegram_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="HIOS",
        version="1.0.0",
    )

    app.include_router(
        chat_router
    )
    app.include_router(
        telegram_router,
    )

    return app


app = create_app()