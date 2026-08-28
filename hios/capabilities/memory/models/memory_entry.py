from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel
from datetime import datetime


class MemoryEntry(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    category: str

    description: str

    confidence: float = 1.0

    importance: float = 0.5

    details: dict[str, str] = Field(
        default_factory=dict,
    )

    access_count: int = 0

    last_accessed_at: datetime | None = None