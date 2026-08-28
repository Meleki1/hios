from __future__ import annotations

from pydantic import Field

from hios.runtime.trace_entry import TraceEntry
from hios.shared.base import HIOSModel


class ProcessTrace(HIOSModel):
    """
    Execution history for a process.
    """

    entries: list[TraceEntry] = Field(
        default_factory=list,
    )

    def append(
        self,
        entry: TraceEntry,
    ) -> None:
        self.entries.append(entry)