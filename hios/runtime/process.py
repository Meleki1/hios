from __future__ import annotations

from uuid import uuid4

from pydantic import Field

from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.runtime.context import RuntimeContext
from hios.runtime.pipeline import Pipeline
from hios.runtime.process_status import ProcessStatus
from hios.shared.base import HIOSModel


class Process(HIOSModel):
    """
    Represents a single execution of a pipeline.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    pipeline: Pipeline

    request: CapabilityRequest

    result: CapabilityResult | None = None

    status: ProcessStatus = ProcessStatus.CREATED

    context: RuntimeContext = Field(
        default_factory=RuntimeContext
    )

    @classmethod
    def start(
        cls,
        *,
        pipeline: Pipeline,
        request: CapabilityRequest,
    ) -> "Process":
        """
        Create a new process ready for execution.
        """
        return cls(
            pipeline=pipeline,
            request=request,
        )

    def running(self) -> "Process":
        """
        Return a copy of the process marked as running.
        """
        return self.model_copy(
            update={
                "status": ProcessStatus.RUNNING,
            }
        )

    def complete(
        self,
        result: CapabilityResult,
    ) -> "Process":
        """
        Return a copy of the process marked as completed.
        """
        return self.model_copy(
            update={
                "status": ProcessStatus.COMPLETED,
                "result": result,
            }
        )

    def cancel(self) -> "Process":
        """
        Return a copy of the process marked as cancelled.
        """
        return self.model_copy(
            update={
                "status": ProcessStatus.CANCELLED,
            }
        )