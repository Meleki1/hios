from pydantic import Field

from hios.shared.base import HIOSModel
from uuid import uuid4


class PredictionEvaluation(HIOSModel):
    
    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    prediction_id: str

    outcome_id: str

    correct: bool

    details: dict[str, str] = Field(
        default_factory=dict,
    )