from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.decision.selector import DecisionSelector
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.contract import PlanResult


class DefaultDecisionSelector(
    DecisionSelector,
):

    def select(
        self,
        plans: PlanResult,
    ) -> Decision | None:

        if not plans.plans:
            return None

        selected = max(
            plans.plans,
            key=self._priority_score,
        )

        return Decision(
            plan=selected,
            rationale="Selected the highest priority plan.",
            score=1.0,
        )

    def _priority_score(
        self,
        plan,
    ) -> int:

        priorities = {
            GoalPriority.CRITICAL: 4,
            GoalPriority.HIGH: 3,
            GoalPriority.MEDIUM: 2,
            GoalPriority.LOW: 1,
        }

        return priorities.get(
            plan.priority,
            0,
        )