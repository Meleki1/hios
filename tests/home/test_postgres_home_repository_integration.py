import pytest
from hios.capabilities.home.models.home import Home
from hios.capabilities.home.repositories.postgres_home_repository import PostgresHomeRepository




@pytest.mark.asyncio
async def test_home_repository_persists_and_retrieves(
    session,
):

    repository = PostgresHomeRepository(
        session=session,
    )

    home = Home(
        name="Integration Test Home",
        home_type="residential",
        description="Test home",
        status="active",
    )

    saved = await repository.save(home)

    result = await repository.get(
        saved.id,
    )

    assert result is not None

    assert result.id == saved.id
    assert result.name == "Integration Test Home"
    assert result.home_type == "residential"
    assert result.description == "Test home"
    assert result.status == "active"