from abc import ABC, abstractmethod


class HomedataClient(ABC):

    @abstractmethod
    async def get_property(
        self,
        uprn: str,
    ) -> dict:
        raise NotImplementedError