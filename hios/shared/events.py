from datetime import datetime
from uuid import UUID

from hios.shared.base import HIOSModel


class DomainEvent(HIOSModel):

    event_id: UUID

    aggregate_id: UUID

    event_type: str

    occurred_at: datetime