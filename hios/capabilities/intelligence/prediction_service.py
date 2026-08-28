from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.prediction_engine import PredictionEngine

from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher


class PredictionService:

    def __init__(
        self,
        engine: PredictionEngine,
        repository,
        event_publisher: EventPublisher | None = None,
    ):
        self._engine = engine
        self._repository = repository
        self._event_publisher = event_publisher

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        prediction = await self._engine.predict(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )

        prediction = await self._repository.save(
            prediction,
        )

        if self._event_publisher is not None:
            await self._event_publisher.publish(
                BaseEvent(
                    event_type="prediction",
                    event_name="prediction_created",
                    state="created",
                    description=(
                        "Prediction created"
                    ),
                    subject_id=prediction.subject_id,
                    resource_id=prediction.id,
                    resource_type="prediction",
                )
            )

        return prediction

        