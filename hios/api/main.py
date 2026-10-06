from fastapi import FastAPI
from contextlib import asynccontextmanager
from pydantic import ValidationError
from hios.api.chat import router as chat_router
from hios.api.telegram import router as telegram_router
from hios.api.bootstrap import router as bootstrap_router
from hios.core.config import get_settings
from hios.runtime.persistence.checkpointer import create_checkpointer


def _validate_settings_or_exit() -> None:
    try:
        get_settings()
    except ValidationError as error:
        raise RuntimeError(
            "HIOS failed to start: invalid or missing configuration.\n"
            f"{error}\n\n"
            "Copy .env.example to .env (or set the equivalent "
            "environment variables in your deploy target) and fill "
            "in the required values -- see .env.example for what "
            "each one is for and where to get it."
        ) from error

@asynccontextmanager
async def lifespan(app: FastAPI):

    async with create_checkpointer() as checkpointer:
        app.state.checkpointer = checkpointer

        yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="HIOS",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.include_router(
        chat_router
    )
    app.include_router(
        telegram_router,
    )
    app.include_router(
        bootstrap_router,
    )


    return app


app = create_app()