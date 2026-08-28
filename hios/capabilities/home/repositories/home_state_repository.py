from abc import ABC, abstractmethod
from hios.capabilities.home.models.home_state import HomeState


class HomeStateRepository(ABC):

    @abstractmethod
    async def save(
        self,
        state: HomeState,
    ) -> HomeState:
        raise NotImplementedError

    @abstractmethod
    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeState | None:
        raise NotImplementedError