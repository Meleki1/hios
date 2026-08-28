from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.execution.models.status import ExecutionStatus

from enum import StrEnum




class ActionType(StrEnum):
    SYSTEM_OPERATION = "system_operation"
    USER_INPUT = "user_input"
    IMAGE_REQUEST = "image_request"


class Action(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str

    description: str

    status: ExecutionStatus = ExecutionStatus.PENDING

    parameters: dict[str, object] = Field(
        default_factory=dict
    )
    action_type: ActionType = ActionType.SYSTEM_OPERATION
