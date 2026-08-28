from datetime import datetime, timezone
from uuid import uuid4
from pydantic import Field
from hios.shared.base import HIOSModel




class Outcome(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    prediction_id: str

    subject_id: str

    target: str

    occurred: bool

    observed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    details: dict[str, str] = Field(
        default_factory=dict,
    )