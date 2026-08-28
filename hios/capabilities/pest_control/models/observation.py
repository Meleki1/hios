from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class PestObservation(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    subject_id: str

    home_id: str

    description: str

    pest_type: str | None = None

    location: str | None = None

    evidence: list[str] = Field(
        default_factory=list,
    )

    source: str = "conversation"