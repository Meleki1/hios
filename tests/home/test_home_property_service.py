import pytest

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)

from hios.capabilities.home.services.home_property_service import (
    HomePropertyService,
)


class FakeHomePropertyReferenceRepository:

    def __init__(self):
        self.saved = []

    async def save(
        self,
        reference: HomePropertyReference,
    ) -> HomePropertyReference:

        self.saved.append(reference)

        return reference

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomePropertyReference | None:

        for reference in self.saved:

            if reference.home_id == home_id:
                return reference

        return None

@pytest.mark.asyncio
async def test_home_property_service_associates_home_with_property():

    repository = (
        FakeHomePropertyReferenceRepository()
    )

    service = HomePropertyService(
        repository=repository,
    )

    result = await service.associate(
        home_id="home-123",
        uprn="100023456789",
    )

    assert result is not None
    assert result.home_id == "home-123"
    assert result.uprn == "100023456789"

    assert len(repository.saved) == 1


@pytest.mark.asyncio
async def test_home_property_service_gets_property_reference_by_home():

    repository = (
        FakeHomePropertyReferenceRepository()
    )

    service = HomePropertyService(
        repository=repository,
    )

    await service.associate(
        home_id="home-123",
        uprn="100023456789",
    )

    result = await service.get_by_home(
        "home-123",
    )

    assert result is not None
    assert result.home_id == "home-123"
    assert result.uprn == "100023456789"


@pytest.mark.asyncio
async def test_home_property_service_returns_none_for_unknown_home():

    repository = (
        FakeHomePropertyReferenceRepository()
    )

    service = HomePropertyService(
        repository=repository,
    )

    result = await service.get_by_home(
        "unknown-home",
    )

    assert result is None