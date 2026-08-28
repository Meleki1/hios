from pydantic import Field

from hios.capabilities.intelligence.models.intent_level import (
    IntentLevel,
)
from hios.capabilities.intelligence.models.signal import (
    Signal,
)
from hios.shared.base import HIOSModel


class IntentScore(HIOSModel):

    score: float

    level: IntentLevel

    confidence: float = 1.0

    signals: list[Signal] = Field(
        default_factory=list,
    )