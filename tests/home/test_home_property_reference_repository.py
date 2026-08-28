import pytest

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)
from hios.capabilities.home.repositories.home_property_reference_repository import (
    HomePropertyReferenceRepository,
)


class FakeHomePropertyReferenceRepository(
    HomePropertyReferenceRepository,
):

    def __init__(self):
        self.saved = {}

    async def save(
        self,
        reference: HomePropertyReference,
    ) -> HomePropertyReference:

        self.saved[reference.home_id] = reference

        return reference

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomePropertyReference | None:

        return self.saved.get(home_id)


@pytest.mark.asyncio
async def test_home_property_reference_repository_saves_and_retrieves():

    repository = (
        FakeHomePropertyReferenceRepository()
    )

    reference = HomePropertyReference(
        home_id="home-123",
        uprn="100023456789",
    )

    saved = await repository.save(
        reference,
    )

    result = await repository.get_by_home(
        "home-123",
    )

    assert saved is reference
    assert result is not None
    assert result.home_id == "home-123"
    assert result.uprn == "100023456789"


@pytest.mark.asyncio
async def test_home_property_reference_repository_returns_none_for_unknown_home():

    repository = (
        FakeHomePropertyReferenceRepository()
    )

    result = await repository.get_by_home(
        "unknown-home",
    )

    assert result is None