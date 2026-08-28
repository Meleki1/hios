from datetime import datetime
from pydantic import Field
from hios.shared.base import HIOSModel


class PlanningApplication(HIOSModel):

    reference: str

    category: str

    status: str

    description: str | None = None

    latitude: float

    longitude: float

    observed_at: datetime

    source: str

    source_url: str | None = None

    metadata: dict[str, str] = Field(
        default_factory=dict,
    )