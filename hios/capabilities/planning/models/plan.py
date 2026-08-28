from hios.shared.base import HIOSModel
from uuid import uuid4
from pydantic import Field
from hios.capabilities.planning.models.task import Task
from hios.capabilities.planning.models.constraint import Constraint
from hios.capabilities.goals.models.priority import GoalPriority

class Plan(HIOSModel):

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    goal_id: str

    name: str

    description: str

    priority: GoalPriority

    tasks: list[Task] = Field(
        default_factory=list
    )

    constraints: list[Constraint] = Field(
        default_factory=list
    )