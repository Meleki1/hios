from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class LearningRecord(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    prediction_id: str

    outcome_id: str

    evaluation_id: str

    target: str

    correct: bool

    signal_names: list[str] = Field(
        default_factory=list,
    )

    signal_values: list[str] = Field(
        default_factory=list,
    )

    signal_strengths: list[float] = Field(
        default_factory=list,
    )

    signal_confidences: list[float] = Field(
        default_factory=list,
    )

    intent_score: float

    prediction_confidence: float

    lesson: str