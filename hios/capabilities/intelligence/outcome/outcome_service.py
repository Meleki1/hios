from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.outcome.outcome_repository import (
    OutcomeRepository,
)


class OutcomeService:

    def __init__(
        self,
        repository: OutcomeRepository,
        event_publisher: EventPublisher | None = None,
    ):
        self._repository = repository
        self._event_publisher = event_publisher

    async def record(
        self,
        outcome: Outcome,
    ) -> Outcome:

        outcome = await self._repository.save(
            outcome,
        )

        if self._event_publisher is not None:
            await self._event_publisher.publish(
                BaseEvent(
                    event_type="outcome",
                    event_name="outcome_recorded",
                    state="observed",
                    description="Outcome recorded",
                    subject_id=outcome.subject_id,
                    resource_id=outcome.id,
                    resource_type="outcome",
                )
            )

        return outcome

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:

        return await self._repository.get_by_prediction(
            prediction_id,
        )