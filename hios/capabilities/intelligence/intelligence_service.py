from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)
from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)


class IntelligenceService:

    def __init__(
        self,
        prediction_service,
        evaluator,
        evaluation_repository,
    ):
        self._prediction_service = prediction_service
        self._evaluator = evaluator
        self._evaluation_repository = evaluation_repository

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        return await self._prediction_service.predict(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:

        evaluation = await self._evaluator.evaluate(
            prediction,
            outcome,
        )

        return await self._evaluation_repository.save(
            evaluation,
        )