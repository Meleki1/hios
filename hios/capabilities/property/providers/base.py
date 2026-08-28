from abc import ABC, abstractmethod

from hios.capabilities.property.models.property_profile import (
    PropertyProfile,
)


class PropertyProvider(ABC):

    @abstractmethod
    async def get_property(
        self,
        uprn: str,
    ) -> PropertyProfile | None:
        raise NotImplementedError

    