from abc import ABC, abstractmethod
from hios.capabilities.home.models.home import Home

class HomeRepository(ABC):

    @abstractmethod
    async def save(
        self,
        home: Home,
    ) -> Home:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        home_id: str,
    ) -> Home | None:
        raise NotImplementedError