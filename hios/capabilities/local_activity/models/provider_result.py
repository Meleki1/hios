from enum import Enum

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.local_activity.models.local_activity_event import (
    LocalActivityEvent,
)


class ProviderStatus(str, Enum):
    SUCCESS = "success"
    UNAVAILABLE = "unavailable"
    PARTIAL = "partial"


class LocalActivityProviderResult(HIOSModel):

    status: ProviderStatus

    events: list[LocalActivityEvent] = Field(
        default_factory=list,
    )

    provider: str

    error: str | None = None