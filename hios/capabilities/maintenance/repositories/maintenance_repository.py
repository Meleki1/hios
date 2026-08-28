from abc import ABC, abstractmethod

from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
)


class MaintenanceRepository(ABC):

    @abstractmethod
    async def save(
        self,
        maintenance: Maintenance,
    ) -> Maintenance:
        ...

    @abstractmethod
    async def get(
        self,
        maintenance_id: str,
    ) -> Maintenance | None:
        ...

    @abstractmethod
    async def get_all(
        self,
    ) -> list[Maintenance]:
        ...

    @abstractmethod
    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[Maintenance]:
        ...

    @abstractmethod
    async def get_by_home(
        self,
        home_id: str,
    ) -> list[Maintenance]:
        ...