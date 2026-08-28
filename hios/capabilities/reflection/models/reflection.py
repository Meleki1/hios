from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.reflection.models.insight import Insight


class Reflection(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    outcome: Outcome

    insights: list[Insight] = Field(
        default_factory=list,
    )

    summary: str = ""

    score: float = 0.0