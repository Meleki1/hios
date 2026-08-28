from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)
from hios.capabilities.intelligence.prediction_evaluator import (
    PredictionEvaluator,
)
from hios.capabilities.intelligence.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)


class PredictionEvaluationService:

    def __init__(
        self,
        evaluator: PredictionEvaluator,
        repository: PredictionEvaluationRepository,
        event_publisher: EventPublisher | None = None,
    ):
        self._evaluator = evaluator
        self._repository = repository
        self._event_publisher = event_publisher

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ) -> PredictionEvaluation:

        evaluation = await self._evaluator.evaluate(
            prediction=prediction,
            outcome=outcome,
        )

        evaluation = await self._repository.save(
            evaluation,
        )

        if self._event_publisher is not None:
            await self._event_publisher.publish(
                BaseEvent(
                    event_type="prediction_evaluation",
                    event_name="prediction_evaluated",
                    state=(
                        "correct"
                        if evaluation.correct
                        else "incorrect"
                    ),
                    description=(
                        "Prediction evaluated"
                    ),
                    subject_id=prediction.subject_id,
                    resource_id=evaluation.id,
                    resource_type=(
                        "prediction_evaluation"
                    ),
                )
            )

        return evaluation