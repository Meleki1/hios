import pytest
from hios.capabilities.intelligence.models.intent_level import IntentLevel
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.intelligence.prediction_service import PredictionService
from hios.capabilities.intelligence.prediction_engine import PredictionEngine
from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher
from hios.capabilities.timeline.listeners.timeline_listener import (
    TimelineListener,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)


class FakeTimelineRepository(
    TimelineRepository,
):

    def __init__(self):
        self.entries = []

    async def save(
        self,
        entry: TimelineEntry,
    ) -> TimelineEntry:

        self.entries.append(entry)

        return entry

    async def get_by_subject(
        self,
        subject_id: str,
    ) -> list[TimelineEntry]:

        return [
            entry
            for entry in self.entries
            if entry.subject_id == subject_id
        ]

        
class FakeEventSubscriber:

    def __init__(self):
        self.events = []

    async def listen(
        self,
        event: BaseEvent,
    ):
        self.events.append(event)


class FakePredictionEngine(PredictionEngine):

    def __init__(self):
        self.received = None

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        intent_score: IntentScore,
    ) -> Prediction:

        self.received = {
            "subject_id": subject_id,
            "target": target,
            "horizon_days": horizon_days,
            "intent_score": intent_score,
        }

        return Prediction(
            id="prediction-integration-1",
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )


class FakePredictionRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        prediction: Prediction,
    ) -> Prediction:

        self.saved = prediction

        return prediction


@pytest.mark.asyncio
async def test_prediction_service_generates_and_persists_prediction():

    engine = FakePredictionEngine()
    repository = FakePredictionRepository()

    service = PredictionService(
        engine=engine,
        repository=repository,
    )

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    result = await service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=90,
        intent_score=intent_score,
    )

    assert result.subject_id == "household-1"
    assert result.target == "pest_control_need"
    assert result.horizon_days == 90

    assert repository.saved is result

    assert engine.received is not None

    assert (
        engine.received["subject_id"]
        == "household-1"
    )

    assert (
        engine.received["target"]
        == "pest_control_need"
    )

    assert (
        engine.received["horizon_days"]
        == 90
    )

    assert (
        engine.received["intent_score"]
        is intent_score
    )


@pytest.mark.asyncio
async def test_prediction_service_publishes_prediction_created_event():

    engine = FakePredictionEngine()
    repository = FakePredictionRepository()

    publisher = EventPublisher()

    subscriber = FakeEventSubscriber()

    publisher.subscribe(subscriber)

    service = PredictionService(
        engine=engine,
        repository=repository,
        event_publisher=publisher,
    )

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    prediction = await service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        intent_score=intent_score,
    )

    assert len(subscriber.events) == 1

    event = subscriber.events[0]

    assert event.event_type == "prediction"
    assert event.event_name == "prediction_created"
    assert event.state == "created"

    assert event.subject_id == (
        prediction.subject_id
    )

    assert event.resource_id == (
        prediction.id
    )

    assert event.resource_type == "prediction"


@pytest.mark.asyncio
async def test_prediction_service_works_without_event_publisher():

    engine = FakePredictionEngine()
    repository = FakePredictionRepository()

    service = PredictionService(
        engine=engine,
        repository=repository,
    )

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    result = await service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        intent_score=intent_score,
    )

    assert result is repository.saved

@pytest.mark.asyncio
async def test_prediction_service_records_prediction_in_timeline():

    engine = FakePredictionEngine()
    prediction_repository = FakePredictionRepository()
    timeline_repository = FakeTimelineRepository()

    publisher = EventPublisher()

    timeline_service = TimelineService(
        repository=timeline_repository,
    )

    timeline_listener = TimelineListener(
        service=timeline_service,
    )

    publisher.subscribe(
        timeline_listener,
    )

    prediction_service = PredictionService(
        engine=engine,
        repository=prediction_repository,
        event_publisher=publisher,
    )

    intent_score = IntentScore(
        score=70.0,
        level=IntentLevel.HIGH,
        confidence=1.0,
        signals=[],
    )

    prediction = await prediction_service.predict(
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        intent_score=intent_score,
    )

    assert len(
        timeline_repository.entries
    ) == 1

    entry = (
        timeline_repository.entries[0]
    )

    assert entry.subject_id == (
        prediction.subject_id
    )

    assert entry.event_type == "prediction"

    assert entry.event_name == (
        "prediction_created"
    )

    assert entry.state == "created"

    assert entry.resource_id == (
        prediction.id
    )

    assert entry.resource_type == (
        "prediction"
    )