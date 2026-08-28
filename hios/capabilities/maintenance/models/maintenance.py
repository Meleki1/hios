from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel


class MaintenanceStatus(str, Enum):
    PLANNED = "planned"
    DUE = "due"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class MaintenanceType(str, Enum):
    ROUTINE = "routine"
    PREVENTIVE = "preventive"
    CONDITION_BASED = "condition_based"
    USER_REQUESTED = "user_requested"


class Maintenance(HIOSModel):
    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    subject_id: str
    home_id: str

    task: str

    maintenance_type: MaintenanceType

    status: MaintenanceStatus = (
        MaintenanceStatus.PLANNED
    )

    scheduled_for: datetime | None = None

    completed_at: datetime | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    evidence: list[str] = Field(
        default_factory=list
    )

    metadata: dict[str, str] = Field(
        default_factory=dict
    )