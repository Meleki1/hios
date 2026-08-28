from abc import ABC, abstractmethod

from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)


class PredictionEvaluationRepository(ABC):

    @abstractmethod
    async def save(
        self,
        evaluation: PredictionEvaluation,
    ) -> PredictionEvaluation:
        raise NotImplementedError

    @abstractmethod
    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> PredictionEvaluation | None:
        raise NotImplementedError