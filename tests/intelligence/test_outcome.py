from hios.capabilities.intelligence.models.outcome import (
    Outcome,
)


def test_outcome_can_be_created():

    outcome = Outcome(
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
    )

    assert outcome.prediction_id == "prediction-1"
    assert outcome.subject_id == "household-1"
    assert outcome.target == "pest_control_need"
    assert outcome.occurred is True