from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)


class OutcomeRepository(ABC):

    @abstractmethod
    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:
        raise NotImplementedError

    @abstractmethod
    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:
        raise NotImplementedError