from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.outcome import Outcome


class OutcomeRecorder(ABC):

    @abstractmethod
    async def record(
        self,
        outcome: Outcome,
    ) -> Outcome:
        raise NotImplementedError