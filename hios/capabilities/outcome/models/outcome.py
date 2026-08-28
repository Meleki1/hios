from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.outcome.models.observation import (
    OutcomeObservation,
)
from hios.capabilities.outcome.models.status import OutcomeStatus


class Outcome(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    execution: Execution

    status: OutcomeStatus = OutcomeStatus.UNKNOWN

    observations: list[
        OutcomeObservation
    ] = Field(
        default_factory=list
    )

    summary: str = ""