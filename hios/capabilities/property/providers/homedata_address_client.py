from abc import ABC, abstractmethod


class HomedataAddressClient(ABC):

    @abstractmethod
    async def search(
        self,
        query: str,
    ) -> list[dict]:
        raise NotImplementedError