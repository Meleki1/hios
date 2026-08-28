from hios.capabilities.understanding.contract import UnderstandingResult
from hios.capabilities.goals.generator import GoalGenerator
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.models.priority import GoalPriority




class DefaultGoalGenerator(GoalGenerator):

    def generate(
        self,
        understanding: UnderstandingResult,
    ) -> list[Goal]:

        goals: dict[str, Goal] = {}

        for hypothesis in understanding.hypotheses:

            if hypothesis.name != "Rodent Infestation":
                continue

            eliminate = Goal(
                id="eliminate_infestation",
                name="Eliminate infestation",
                description="Remove the rodent infestation.",
                priority=GoalPriority.CRITICAL,
                source_hypothesis=hypothesis.id,
            )

            prevent = Goal(
                id="prevent_recurrence",
                name="Prevent recurrence",
                description="Prevent future infestations.",
                priority=GoalPriority.HIGH,
                source_hypothesis=hypothesis.id,
            )

            goals.setdefault(
                eliminate.id,
                eliminate,
            )

            goals.setdefault(
                prevent.id,
                prevent,
            )

        return list(goals.values())