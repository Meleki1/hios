import pytest_asyncio


@pytest_asyncio.fixture(
    scope="session",
    loop_scope="session",
    autouse=True,
)
async def setup_database():
    """Unit tests in this project do not require Postgres."""
    yield
