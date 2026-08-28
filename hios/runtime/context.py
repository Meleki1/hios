from __future__ import annotations
from datetime import datetime, UTC
from uuid import uuid4
from hios.memory.working_memory import WorkingMemory

from pydantic import Field

from hios.shared.base import HIOSModel
from typing import Any

class RuntimeContext(HIOSModel):
    """
    Shared execution context for a single pipeline execution.
    """

    execution_id: str = Field(default_factory=lambda: str(uuid4()))
    working_memory: WorkingMemory = Field(default_factory=WorkingMemory)
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )