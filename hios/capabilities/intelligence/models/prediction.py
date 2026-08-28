from pydantic import Field
from uuid import uuid4
from hios.shared.base import HIOSModel
from hios.capabilities.intelligence.models.intent_score import (
    IntentScore,
)


class Prediction(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )
    subject_id: str

    target: str

    horizon_days: int

    intent_score: IntentScore

    probability: float | None = None

    confidence: float = 1.0

    evidence: list[str] = Field(
        default_factory=list,
    )