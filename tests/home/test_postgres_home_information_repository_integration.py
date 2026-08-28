import pytest
from uuid import uuid4

from hios.capabilities.home.models.home_information import (
    HomeInformation,
)

from hios.capabilities.home.repositories.postgres_home_information_repository import (
    PostgresHomeInformationRepository,
)
from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)


@pytest.mark.asyncio
async def test_home_information_repository_persists_and_retrieves(
    session,
):

    repository = (
        PostgresHomeInformationRepository(
            session=session,
        )
    )

    home_id = str(uuid4())

    home = HomeRecord(
        id=home_id,
        name="Integration Test Home",
        home_type="residential",
        description="Test home",
        status="active",
    )

    session.add(home)

    await session.commit()

    information = HomeInformation(
        home_id=home_id,
        country="United Kingdom",
        city="London",
        address="10 Integration Road",
        postcode="SW1A 1AA",
    )

    saved = await repository.save(
        information,
    )

    result = await repository.get_by_home(
        saved.home_id,
    )

    assert result is not None

    assert result.id == saved.id
    assert result.home_id == home_id
    assert result.country == "United Kingdom"
    assert result.city == "London"
    assert result.address == "10 Integration Road"
    assert result.postcode == "SW1A 1AA"

@pytest.mark.asyncio
async def test_home_information_repository_returns_none_for_unknown_home(
    session,
):

    repository = (
        PostgresHomeInformationRepository(
            session=session,
        )
    )

    result = await repository.get_by_home(
        "does-not-exist",
    )

    assert result is None