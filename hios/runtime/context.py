from __future__ import annotations
from datetime import datetime, UTC
from uuid import uuid4
from typing import Any

from pydantic import Field

from hios.shared.base import HIOSModel


class RuntimeContext(HIOSModel):
    """
    Shared execution context for a single pipeline execution.
    """

    execution_id: str = Field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))