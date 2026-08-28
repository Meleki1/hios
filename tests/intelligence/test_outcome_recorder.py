import pytest

from hios.capabilities.intelligence.basic_outcome_recorder import (
    BasicOutcomeRecorder,
)
from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)


@pytest.mark.asyncio
async def test_outcome_recorder_returns_recorded_outcome():

    recorder = BasicOutcomeRecorder()

    outcome = Outcome(
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    result = await recorder.record(outcome)

    assert result.id == outcome.id
    assert result.prediction_id == "prediction-1"
    assert result.subject_id == "household-1"
    assert result.target == "pest_control_need"
    assert result.occurred is True