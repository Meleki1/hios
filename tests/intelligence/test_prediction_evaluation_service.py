
import pytest

from hios.core.events.base_event import BaseEvent
from hios.core.events.event_publisher import EventPublisher

from hios.capabilities.intelligence.basic_prediction_evaluator import (
    BasicPredictionEvaluator,
)

from hios.capabilities.intelligence.prediction_evaluation_service import (
    PredictionEvaluationService,
)

from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)

from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)

from hios.capabilities.intelligence.models.intent_score import (
    IntentLevel,
    IntentScore,
)

from hios.capabilities.intelligence.models.prediction_evaluation import (
    PredictionEvaluation,
)

from hios.capabilities.intelligence.prediction_evaluation_repository import (
    PredictionEvaluationRepository,
)

from hios.capabilities.timeline.models.timeline_entry import (
    TimelineEntry,
)
from hios.capabilities.timeline.services.timeline_service import (
    TimelineService,
)
from hios.capabilities.timeline.repositories.timeline_repository import (
    TimelineRepository,
)
from hios.capabilities.timeline.listeners.timeline_listener import TimelineListener


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


class FakePredictionEvaluationRepository(
    PredictionEvaluationRepository,
):

    def __init__(self):
        self.saved = None
        self.evaluations = []

    async def save(
        self,
        evaluation: PredictionEvaluation,
    ) -> PredictionEvaluation:

        self.saved = evaluation
        self.evaluations.append(evaluation)

        return evaluation
        

    async def get_by_prediction(
        self,
        prediction_id: str,
    ) -> PredictionEvaluation | None:

        for evaluation in self.evaluations:
            if evaluation.prediction_id == prediction_id:
                return evaluation

        return None


class FakeSubscriber:

    def __init__(self):
        self.events = []

    async def listen(
        self,
        event: BaseEvent,
    ):
        self.events.append(event)


def make_prediction() -> Prediction:

    return Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=14,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=1.0,
            signals=[],
        ),
    )


def make_outcome(
    prediction_id: str,
    occurred: bool,
) -> Outcome:

    return Outcome(
        id="outcome-1",
        prediction_id=prediction_id,
        subject_id="household-1",
        target="pest_control_need",
        occurred=occurred,
    )




@pytest.mark.asyncio
async def test_prediction_evaluation_service_evaluates_and_persists():

    evaluator = BasicPredictionEvaluator()
    repository = FakePredictionEvaluationRepository()

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=repository,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=True,
    )

    result = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.prediction_id == prediction.id
    assert result.outcome_id == outcome.id
    assert result.correct is True

    assert repository.saved is result


@pytest.mark.asyncio
async def test_prediction_evaluation_service_persists_incorrect_evaluation():

    evaluator = BasicPredictionEvaluator()
    repository = FakePredictionEvaluationRepository()

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=repository,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=False,
    )

    result = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.correct is False
    assert repository.saved is result


@pytest.mark.asyncio
async def test_prediction_evaluation_service_publishes_event():

    evaluator = BasicPredictionEvaluator()
    repository = FakePredictionEvaluationRepository()

    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=repository,
        event_publisher=publisher,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=True,
    )

    evaluation = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert len(subscriber.events) == 1

    event = subscriber.events[0]

    assert event.event_type == (
        "prediction_evaluation"
    )

    assert event.event_name == (
        "prediction_evaluated"
    )

    assert event.state == "correct"

    assert event.subject_id == (
        prediction.subject_id
    )

    assert event.resource_id == (
        evaluation.id
    )

    assert event.resource_type == (
        "prediction_evaluation"
    )

@pytest.mark.asyncio
async def test_prediction_evaluation_service_publishes_incorrect_state():

    evaluator = BasicPredictionEvaluator()
    repository = FakePredictionEvaluationRepository()

    publisher = EventPublisher()
    subscriber = FakeSubscriber()

    publisher.subscribe(subscriber)

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=repository,
        event_publisher=publisher,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=False,
    )

    await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    event = subscriber.events[0]

    assert event.state == "incorrect"


@pytest.mark.asyncio
async def test_prediction_evaluation_service_records_evaluation_in_timeline():

    evaluator = BasicPredictionEvaluator()
    evaluation_repository = (
        FakePredictionEvaluationRepository()
    )
    timeline_repository = (
        FakeTimelineRepository()
    )

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

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=evaluation_repository,
        event_publisher=publisher,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=True,
    )

    evaluation = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    assert len(
        timeline_repository.entries
    ) == 1

    entry = timeline_repository.entries[0]

    assert entry.subject_id == (
        prediction.subject_id
    )

    assert entry.event_type == (
        "prediction_evaluation"
    )

    assert entry.event_name == (
        "prediction_evaluated"
    )

    assert entry.state == "correct"

    assert entry.resource_id == (
        evaluation.id
    )

    assert entry.resource_type == (
        "prediction_evaluation"
    )


@pytest.mark.asyncio
async def test_prediction_evaluation_service_records_incorrect_evaluation_in_timeline():

    evaluator = BasicPredictionEvaluator()
    evaluation_repository = (
        FakePredictionEvaluationRepository()
    )
    timeline_repository = (
        FakeTimelineRepository()
    )

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

    service = PredictionEvaluationService(
        evaluator=evaluator,
        repository=evaluation_repository,
        event_publisher=publisher,
    )

    prediction = make_prediction()

    outcome = make_outcome(
        prediction_id=prediction.id,
        occurred=False,
    )

    evaluation = await service.evaluate(
        prediction=prediction,
        outcome=outcome,
    )

    entry = timeline_repository.entries[0]

    assert evaluation.correct is False
    assert entry.state == "incorrect"


