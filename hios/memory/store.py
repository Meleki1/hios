from abc import ABC, abstractmethod

from hios.memory.memory_record import MemoryRecord


class MemoryStore(ABC):

    @abstractmethod
    def save(
        self,
        memory: MemoryRecord,
    ) -> None:
        ...

    @abstractmethod
    def load(
        self,
        key: str,
    ) -> MemoryRecord | None:
        ...

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        ...

    @abstractmethod
    def list(
        self,
        namespace: str,
    ) -> list[MemoryRecord]:
        ...