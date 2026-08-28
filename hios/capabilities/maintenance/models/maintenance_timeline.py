from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MaintenanceTimelineItemType(str, Enum):
    MAINTENANCE = "maintenance"
    RECOMMENDATION = "recommendation"


class MaintenanceTimelineItem(BaseModel):
    subject_id: str
    home_id: str

    task: str
    item_type: MaintenanceTimelineItemType

    status: str

    scheduled_for: datetime | None = None
    recommended_for: datetime | None = None

    maintenance_type: str

    reason: str | None = None
    priority: str | None = None

    source_signals: list[str] = []
    metadata: dict[str, str] = {}