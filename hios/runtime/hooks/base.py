from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hios.runtime.process import Process


class PipelineHook(ABC):
    """
    Executes before or after a pipeline.
    """

    @abstractmethod
    async def execute(
        self,
        process: Process
    ) -> None:
        ...