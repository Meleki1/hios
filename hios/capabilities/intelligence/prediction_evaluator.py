from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)


class PredictionEvaluator(ABC):

    @abstractmethod
    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:
        raise NotImplementedError