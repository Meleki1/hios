from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class PestAssessment(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    observation_id: str

    pest_type: str | None = None

    confidence: float = 0.0

    severity: str | None = None

    explanation: str = ""

    indicators: list[str] = Field(
        default_factory=list,
    )