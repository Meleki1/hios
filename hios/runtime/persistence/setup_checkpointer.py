import asyncio

from hios.runtime.persistence.checkpointer import (
    create_checkpointer,
)


async def main() -> None:
    async with create_checkpointer() as checkpointer:
        await checkpointer.setup()


if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=asyncio.SelectorEventLoop,
    )