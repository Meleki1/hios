import pytest

from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher
from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)

from hios.capabilities.intelligence.outcome.outcome_repository import (
    OutcomeRepository,
)

class FakeOutcomeRepository(
    OutcomeRepository,
):

    def __init__(self):
        self.saved = None
        self.outcomes = []

    async def save(
        self,
        outcome: Outcome,
    ) -> Outcome:

        self.saved = outcome
        self.outcomes.append(outcome)

        return outcome

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> Outcome | None:

        for outcome in self.outcomes:
            if outcome.prediction_id == prediction_id:
                return outcome

        return None


class FakeSubscriber:

    def __init__(self):
        self.received = []

    async def listen(
        self,
        event: BaseEvent,
    ) -> None:

        self.received.append(event)


@pytest.mark.asyncio
async def test_event_publisher_delivers_event():

    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    event = BaseEvent(
        event_type="prediction",
        event_name="prediction_created",
        state="created",
        description="Prediction created",
        subject_id="household-1",
        resource_id="prediction-1",
        resource_type="prediction",
    )

    await publisher.publish(event)

    assert len(subscriber.received) == 1

    assert subscriber.received[0] is event

    assert (
        subscriber.received[0].subject_id
        == "household-1"
    )

    assert (
        subscriber.received[0].resource_id
        == "prediction-1"
    )


@pytest.mark.asyncio
async def test_event_publisher_supports_multiple_subscribers():

    publisher = EventPublisher()

    first = FakeSubscriber()
    second = FakeSubscriber()

    publisher.subscribe(first)
    publisher.subscribe(second)

    event = BaseEvent(
        event_type="outcome",
        event_name="outcome_recorded",
        state="observed",
        description="Outcome recorded",
        subject_id="household-1",
        resource_id="outcome-1",
        resource_type="outcome",
    )

    await publisher.publish(event)

    assert first.received == [event]
    assert second.received == [event]


