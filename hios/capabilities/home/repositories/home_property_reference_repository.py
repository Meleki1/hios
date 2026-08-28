from abc import ABC, abstractmethod

from hios.capabilities.home.models.home_property_reference import (
    HomePropertyReference,
)


class HomePropertyReferenceRepository(ABC):

    @abstractmethod
    async def save(
        self,
        reference: HomePropertyReference,
    ) -> HomePropertyReference:
        raise NotImplementedError

    @abstractmethod
    async def get_by_home(
        self,
        home_id: str,
    ) -> HomePropertyReference | None:
        raise NotImplementedError