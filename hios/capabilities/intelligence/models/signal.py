from datetime import datetime, timezone
from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class Signal(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    type: SignalType
    source: SignalSource
    name: str
    value: str
    strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )
    observed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
    )
