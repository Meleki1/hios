import pytest

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)

from hios.capabilities.home.repositories.postgres_home_property_reference_repository import (
    PostgresHomePropertyReferenceRepository,
)

from hios.capabilities.home.persistence.models.home_record import (
    HomeRecord,
)
from sqlalchemy.exc import IntegrityError


@pytest.mark.asyncio
async def test_home_property_reference_repository_persists_and_retrieves(
    session,
):

    repository = (
        PostgresHomePropertyReferenceRepository(
            session=session,
        )
    )

    home = HomeRecord(
        id="home-property-100",
        name="Property Association Home",
        home_type="residential",
        description="Test home",
        status="active",
    )

    session.add(home)

    await session.commit()

    reference = HomePropertyReference(
        home_id="home-property-100",
        uprn="100023456789",
    )

    saved = await repository.save(
        reference,
    )

    result = await repository.get_by_home(
        "home-property-100",
    )

    assert result is not None

    assert result.id == saved.id

    assert result.home_id == (
        "home-property-100"
    )

    assert result.uprn == (
        "100023456789"
    )


@pytest.mark.asyncio
async def test_home_property_reference_repository_returns_none_for_unknown_home(
    session,
):

    repository = (
        PostgresHomePropertyReferenceRepository(
            session=session,
        )
    )

    result = await repository.get_by_home(
        "unknown-home-property",
    )

    assert result is None

@pytest.mark.asyncio
async def test_home_property_reference_repository_rejects_duplicate_home(
    session,
):

    repository = (
        PostgresHomePropertyReferenceRepository(
            session=session,
        )
    )

    home = HomeRecord(
        id="home-property-200",
        name="Duplicate Association Home",
        home_type="residential",
        description=None,
        status="active",
    )

    session.add(home)

    await session.commit()

    first = HomePropertyReference(
        home_id="home-property-200",
        uprn="100023456789",
    )

    await repository.save(
        first,
    )

    second = HomePropertyReference(
        home_id="home-property-200",
        uprn="100098765432",
    )

    with pytest.raises(IntegrityError):
        try:
            await repository.save(
                second,
            )
        except IntegrityError:
            await session.rollback()
            raise