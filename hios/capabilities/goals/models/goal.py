from uuid import uuid4

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.goals.models.status import GoalStatus


class Goal(HIOSModel):
    """
    Desired outcome inferred from understanding.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    name: str

    description: str

    priority: GoalPriority = GoalPriority.MEDIUM

    status: GoalStatus = GoalStatus.PENDING

    source_hypothesis: str | None = None