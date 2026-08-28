from pydantic import Field

from hios.shared.base import HIOSModel


class SignalPerformance(HIOSModel):

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