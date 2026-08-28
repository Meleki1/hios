from uuid import uuid4
from pydantic import Field
from hios.shared.base import HIOSModel


class LearningInsight(HIOSModel):
    id: str = Field(
        default_factory=lambda: str(uuid4()),
    )

    target: str
    signal_name: str

    sample_size: int = Field(ge=0)
    correct_count: int = Field(ge=0)
    incorrect_count: int = Field(ge=0)

    accuracy: float = Field(
        ge=0.0,
        le=1.0,
    )

    insight: str