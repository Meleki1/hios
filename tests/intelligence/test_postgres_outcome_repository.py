from datetime import UTC, datetime

from hios.capabilities.intelligence.models.outcome import Outcome
from hios.capabilities.intelligence.postgres.models.outcome import (
    OutcomeRecord,
)
from hios.capabilities.intelligence.postgres.repository import (
    PostgresOutcomeRepository,
)


def test_outcome_record_maps_to_domain():

    observed_at = datetime.now(UTC)

    record = OutcomeRecord(
        id="outcome-1",
        prediction_id="prediction-1",
        subject_id="household-1",
        target="pest_control_need",
        occurred=True,
        observed_at=observed_at,
        details={
            "service_requested": "true",
        },
    )

    outcome = PostgresOutcomeRepository._to_domain(
        record,
    )

    assert isinstance(outcome, Outcome)

    assert outcome.id == "outcome-1"
    assert outcome.prediction_id == "prediction-1"
    assert outcome.subject_id == "household-1"
    assert outcome.target == "pest_control_need"
    assert outcome.occurred is True
    assert outcome.observed_at == observed_at
    assert outcome.details == {
        "service_requested": "true",
    }