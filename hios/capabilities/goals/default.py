from hios.capabilities.understanding.contract import UnderstandingResult
from hios.capabilities.understanding.models.hypothesis import HypothesisStatus
from hios.capabilities.goals.generator import GoalGenerator
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.models.priority import GoalPriority




class DefaultGoalGenerator(GoalGenerator):

    def generate(
        self,
        understanding: UnderstandingResult,
    ) -> list[Goal]:

        goals: dict[str, Goal] = {}

        for unknown in understanding.unknowns:
            goal = Goal(
                id="investigate_issue",
                name="Understand the reported issue",
                description=unknown.description,
                priority=GoalPriority.HIGH,
                source_hypothesis=None,
            )

            goals.setdefault(
                goal.id,
                goal,
            )
        for hypothesis in understanding.hypotheses:

            if hypothesis.status == HypothesisStatus.CONFIRMED:
                goal = Goal(
                    id=f"address_confirmed_{hypothesis.id}",
                    name=f"Address {hypothesis.name}",
                    description=(
                        f"Recommend remediation for the confirmed "
                        f"{hypothesis.name.lower()}."
                    ),
                    priority=GoalPriority.CRITICAL,
                    source_hypothesis=hypothesis.id,
                )
            else:
                goal = Goal(
                    id=f"gather_evidence_{hypothesis.id}",
                    name="Gather visual evidence",
                    description=(
                        f"Gather visual evidence to better "
                        f"understand the suspected "
                        f"{hypothesis.name.lower()}."
                    ),
                    priority=GoalPriority.HIGH,
                    source_hypothesis=hypothesis.id,
                )

            goals.setdefault(
                goal.id,
                goal,
            )

        return list(goals.values())