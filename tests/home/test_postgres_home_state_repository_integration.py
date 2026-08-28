import pytest

from hios.capabilities.home.models.home_state import (
    HomeState,
)

from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)

from hios.capabilities.home.repositories.postgres_home_state_repository import (
    PostgresHomeStateRepository,
)


@pytest.mark.asyncio
async def test_home_state_repository_persists_and_retrieves(
    session,
):

    repository = (
        PostgresHomeStateRepository(
            session=session,
        )
    )

    home = HomeRecord(
        id="home-state-repository-0070",
        name="Integration Test Home",
        home_type="residential",
        description="Test home",
        status="active",
    )

    session.add(home)

    await session.commit()

    state = HomeState(
        home_id="home-state-repository-0070",
        status="active",
    )

    saved = await repository.save(
        state,
    )

    result = await repository.get_by_home(
        saved.home_id,
    )

    assert result is not None

    assert result.id == saved.id
    assert result.home_id == (
        "home-state-repository-0070"
    )
    assert result.status == "active"


@pytest.mark.asyncio
async def test_home_state_repository_returns_none_for_unknown_home(
    session,
):

    repository = (
        PostgresHomeStateRepository(
            session=session,
        )
    )

    result = await repository.get_by_home(
        "does-not-exist",
    )

    assert result is None