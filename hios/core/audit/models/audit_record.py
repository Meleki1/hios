from datetime import datetime, timezone
from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class AuditRecord(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    event_type: str
    event_name: str
    state: str
    description: str

    subject_id: str

    resource_id: str | None = None
    resource_type: str | None = None

    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    details: dict[str, str] = Field(
        default_factory=dict
    )