"""import pytest

from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)
from hios.capabilities.intelligence.models.prediction import (
    Prediction,
)
from hios.capabilities.learning.models.learning_record import (
    LearningRecord,
)
from hios.capabilities.learning.workflow import (
    LearningWorkflow,
)


class FakeLearningService:

    def __init__(self):
        self.received_prediction = None
        self.received_outcome = None
        self.received_evaluation = None

    async def learn_from_prediction(
        self,
        prediction,
        outcome,
        evaluation,
    ) -> LearningRecord:

        self.received_prediction = prediction
        self.received_outcome = outcome
        self.received_evaluation = evaluation

        return LearningRecord(
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            evaluation_id=evaluation.id,
            target=prediction.target,
            correct=evaluation.correct,
            signal_names=[],
            signal_values=[],
            signal_strengths=[],
            signal_confidences=[],
            intent_score=prediction.intent_score.score,
            prediction_confidence=prediction.confidence,
            lesson="Prediction was correct.",
        )


class FakeLearningRepository:

    def __init__(self):
        self.saved = None

    async def save(
        self,
        record: LearningRecord,
    ) -> LearningRecord:

        self.saved = record

        return record


class FakeIntelligenceService:

    def __init__(self):
        self.received_prediction = None
        self.received_outcome = None

    async def evaluate(
        self,
        prediction: Prediction,
        outcome: Outcome,
    ):
        self.received_prediction = prediction
        self.received_outcome = outcome

        from hios.capabilities.intelligence.models.prediction_evaluation import (
            PredictionEvaluation,
        )

        return PredictionEvaluation(
            id="evaluation-1",
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            correct=outcome.occurred,
        )


def make_prediction() -> Prediction:

    from hios.capabilities.intelligence.models.intent_level import (
        IntentLevel,
    )
    from hios.capabilities.intelligence.models.intent_score import (
        IntentScore,
    )

    return Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=[],
        ),
        confidence=0.9,
    )


def make_outcome() -> Outcome:

    return Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )


@pytest.mark.asyncio
async def test_learning_workflow_evaluates_and_creates_learning_record():

    intelligence_service = FakeIntelligenceService()
    learning_service = FakeLearningService()
    learning_repository = FakeLearningRepository()

    workflow = LearningWorkflow(
        intelligence_service=intelligence_service,
        learning_service=learning_service,
        learning_repository=learning_repository,
    )

    prediction = make_prediction()
    outcome = make_outcome()

    result = await workflow.process(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.prediction_id == prediction.id

    assert result.outcome_id == outcome.id

    assert result.evaluation_id == "evaluation-1"

    assert result.target == (
        "pest_control_need"
    )

    assert result.correct is True

    assert (
        intelligence_service.received_prediction
        is prediction
    )

    assert (
        intelligence_service.received_outcome
        is outcome
    )

    assert (
        learning_service.received_prediction
        is prediction
    )

    assert (
        learning_service.received_outcome
        is outcome
    )

    assert (
        learning_service.received_evaluation.id
        == "evaluation-1"
    )

    assert (
        learning_repository.saved
        is result
    )"""

import pytest

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.learning.models.learning_record import LearningRecord
from hios.capabilities.learning.workflow import LearningWorkflow
from hios.capabilities.learning.learning_service import (
    LearningService,
)
from hios.capabilities.intelligence.models.prediction_evaluation import (
            PredictionEvaluation,
        )

class FakeIntelligenceService:

    def __init__(self):
        self.received_prediction = None
        self.received_outcome = None

    async def evaluate(
        self,
        prediction,
        outcome,
    ):
        self.received_prediction = prediction
        self.received_outcome = outcome

        return PredictionEvaluation(
            id="evaluation-1",
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            correct=outcome.occurred,
        )


class FakeLearningService:

    def __init__(self):
        self.received_prediction = None
        self.received_outcome = None
        self.received_evaluation = None

    async def learn_from_prediction(
        self,
        prediction,
        outcome,
        evaluation,
    ) -> LearningRecord:

        self.received_prediction = prediction
        self.received_outcome = outcome
        self.received_evaluation = evaluation

        return LearningRecord(
            prediction_id=prediction.id,
            outcome_id=outcome.id,
            evaluation_id=evaluation.id,
            target=prediction.target,
            correct=evaluation.correct,
            signal_names=[],
            signal_values=[],
            signal_strengths=[],
            signal_confidences=[],
            intent_score=prediction.intent_score.score,
            prediction_confidence=prediction.confidence,
            lesson="Prediction was correct.",
        )


class FakeLearningRepository:

    def __init__(self):
        self.saved = []

    async def save(
        self,
        record: LearningRecord,
    ) -> LearningRecord:
        self.saved.append(record)
        return record


def make_prediction() -> Prediction:
    from hios.capabilities.intelligence.models.intent_level import (
        IntentLevel,
    )
    from hios.capabilities.intelligence.models.intent_score import (
        IntentScore,
    )

    return Prediction(
        id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        horizon_days=30,
        intent_score=IntentScore(
            score=70.0,
            level=IntentLevel.HIGH,
            confidence=0.9,
            signals=[],
        ),
        confidence=0.9,
    )


def make_outcome() -> Outcome:
    return Outcome(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )


@pytest.mark.asyncio
async def test_learning_workflow_evaluates_learns_and_persists():

    intelligence_service = FakeIntelligenceService()
    learning_service = FakeLearningService()
    learning_repository = FakeLearningRepository()

    workflow = LearningWorkflow(
        intelligence_service=intelligence_service,
        learning_service=learning_service,
        learning_repository=learning_repository,
    )

    prediction = make_prediction()
    outcome = make_outcome()

    result = await workflow.process(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.prediction_id == prediction.id
    assert result.outcome_id == outcome.id
    assert result.evaluation_id == "evaluation-1"
    assert result.target == "pest_control_need"
    assert result.correct is True

    assert (
        intelligence_service.received_prediction
        is prediction
    )

    assert (
        intelligence_service.received_outcome
        is outcome
    )

    assert (
        learning_service.received_prediction
        is prediction
    )

    assert (
        learning_service.received_outcome
        is outcome
    )

    assert (
        learning_service.received_evaluation.id
        == "evaluation-1"
    )

    assert learning_repository.saved is result

@pytest.mark.asyncio
async def test_learning_workflow_processes_prediction_into_learning_record():
    intelligence_service = FakeIntelligenceService()
    learning_service = LearningService()
    repository = FakeLearningRepository()

    workflow = LearningWorkflow(
        intelligence_service=intelligence_service,
        learning_service=learning_service,
        learning_repository=repository,
    )

    prediction = make_prediction()
    outcome = make_outcome()
    
    result = await workflow.process(
        prediction=prediction,
        outcome=outcome,
    )

    assert result.prediction_id == prediction.id
    assert result.outcome_id == outcome.id
    assert result.target == prediction.target
    assert repository.saved[0] is result