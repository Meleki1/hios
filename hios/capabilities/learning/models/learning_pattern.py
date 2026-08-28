from pydantic import Field
from hios.capabilities.learning.models.signal_performance import (
    SignalPerformance,
)
from hios.shared.base import HIOSModel


class LearningPattern(HIOSModel):

    target: str

    sample_size: int = Field(
        ge=0,
    )

    correct_count: int = Field(
        ge=0,
    )

    incorrect_count: int = Field(
        ge=0,
    )

    accuracy: float = Field(
        ge=0.0,
        le=1.0,
    )

    lesson: str

    signal_performance: dict[
        str,
        SignalPerformance,
    ] = Field(
        default_factory=dict,
    )