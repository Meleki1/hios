from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)

from hios.capabilities.home.repositories.home_property_reference_repository import (
    HomePropertyReferenceRepository,
)


class HomePropertyService:

    def __init__(
        self,
        repository: HomePropertyReferenceRepository,
    ):
        self._repository = repository

    async def associate(
        self,
        home_id: str,
        uprn: str,
    ) -> HomePropertyReference:

        reference = HomePropertyReference(
            home_id=home_id,
            uprn=uprn,
        )

        return await self._repository.save(
            reference,
        )

    async def get_by_home(
        self,
        home_id: str,
    ) -> HomePropertyReference | None:

        return await self._repository.get_by_home(
            home_id,
        )