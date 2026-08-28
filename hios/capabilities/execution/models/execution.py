from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.execution.models.action import Action
from hios.capabilities.execution.models.status import ExecutionStatus


class Execution(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    decision: Decision

    status: ExecutionStatus = ExecutionStatus.PENDING

    actions: list[Action] = Field(
        default_factory=list
    )