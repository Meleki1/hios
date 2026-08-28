from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.signal import Signal


class IntentScorer(ABC):

    @abstractmethod
    async def score(
        self,
        signals: list[Signal],
    ) -> IntentScore:
        raise NotImplementedError