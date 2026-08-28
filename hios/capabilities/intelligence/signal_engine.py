from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.signal import Signal


class SignalEngine(ABC):

    @abstractmethod
    async def collect(
        self,
        subject_id: str,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
    ) -> list[Signal]:
        raise NotImplementedError