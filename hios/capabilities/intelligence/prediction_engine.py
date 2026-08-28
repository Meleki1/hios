from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)


class PredictionEngine(ABC):

    @abstractmethod
    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:
        raise NotImplementedError