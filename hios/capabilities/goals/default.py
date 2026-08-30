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

            if hypothesis.name == "Rodent Infestation":
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

            elif hypothesis.name == "Possible Rodent Activity":
                investigate = Goal(
                    id="investigate_rodent_activity",
                    name="Gather visual evidence",
                    description=(
                        "Gather visual evidence to better understand "
                        "the possible rodent activity."
                    ),
                    priority=GoalPriority.HIGH,
                    source_hypothesis=hypothesis.id,
                )

                goals.setdefault(
                    investigate.id,
                    investigate,
                )
        

        return list(goals.values())