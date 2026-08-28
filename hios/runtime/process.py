from __future__ import annotations

from uuid import uuid4

from pydantic import Field

from hios.contracts.requests import CapabilityRequest
from hios.contracts.results import CapabilityResult
from hios.runtime.context import RuntimeContext
from hios.runtime.process_status import ProcessStatus
from hios.runtime.trace import ProcessTrace
from hios.shared.base import HIOSModel


class Process(HIOSModel):
    """
    Represents one execution of HIOS.
    Holds execution state only.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    request: CapabilityRequest

    result: CapabilityResult | None = None

    status: ProcessStatus = ProcessStatus.CREATED

    context: RuntimeContext = Field(
        default_factory=RuntimeContext
    )

    trace: ProcessTrace = Field(
        default_factory=ProcessTrace
    )

    @classmethod
    def start(
        cls,
        *,
        request: CapabilityRequest,
    ) -> "Process":

        return cls(
            request=request,
        )

    def running(self) -> "Process":

        return self.model_copy(
            update={
                "status": ProcessStatus.RUNNING,
            }
        )

    def complete(
        self,
        result: CapabilityResult,
    ) -> "Process":

        return self.model_copy(
            update={
                "status": ProcessStatus.COMPLETED,
                "result": result,
            }
        )

    def cancel(self) -> "Process":

        return self.model_copy(
            update={
                "status": ProcessStatus.CANCELLED,
            }
        )

    def fail(
        self,
    ) -> "Process":

        return self.model_copy(
            update={
                "status": ProcessStatus.FAILED,
            }
        )