from abc import ABC, abstractmethod
from hios.capabilities.home.models.home_information import HomeInformation

class HomeInformationRepository(ABC):

    @abstractmethod
    async def save(
        self,
        information: HomeInformation,
    ) -> HomeInformation:
        raise NotImplementedError

    @abstractmethod
    async def get_by_home(
        self,
        home_id: str,
    ) -> HomeInformation | None:
        raise NotImplementedError