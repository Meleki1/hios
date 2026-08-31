from fastapi import FastAPI
from contextlib import asynccontextmanager
from hios.api.chat import router as chat_router
from hios.api.telegram import router as telegram_router
from hios.api.bootstrap import router as bootstrap_router
from hios.runtime.persistence.checkpointer import create_checkpointer


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