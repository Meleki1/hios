from datetime import datetime, timezone
from typing import Any

from pydantic import Field

from hios.shared.base import HIOSModel


class MemoryRecord(HIOSModel):
    """
    One stored memory.
    """

    namespace: str = "default"

    key: str

    value: Any

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )