from __future__ import annotations

from pydantic import Field

from hios.shared.base import HIOSModel

from hios.contracts.requests import CapabilityRequest

from hios.capabilities.knowledge.contract import (
    KnowledgeResult,
)

from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)

from hios.capabilities.goals.contract import (
    GoalResult,
)


class HIOSState(HIOSModel):
    """
    Shared cognitive state for a single HIOS execution.
    """

    request: CapabilityRequest

    knowledge: KnowledgeResult | None = None

    understanding: UnderstandingResult | None = None

    goals: GoalResult | None = None

    metadata: dict[str, object] = Field(
        default_factory=dict,
    )

    @property
    def has_knowledge(self) -> bool:

        return self.knowledge is not None

    @property
    def has_understanding(self) -> bool:

        return self.understanding is not None

    @property
    def has_goals(self) -> bool:

        return self.goals is not None