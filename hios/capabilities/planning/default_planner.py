from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.planning.models.constraint import Constraint
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.models.task import Task
from hios.capabilities.planning.planner import Planner
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.memory.investigation.question import (
    InvestigationQuestion,
)

class DefaultPlanner(Planner):

    def create(
        self,
        goals: GoalResult,
        investigation_question: InvestigationQuestion | None = None,
    ) -> list[Plan]:

        plans: dict[str, Plan] = {}

        for goal in goals.goals:

            if goal.id == "investigate_issue":
                if investigation_question is not None:
                    task = Task(
                        name="Ask Investigation Question",
                        description=investigation_question.question,
                        required=True,
                    )
                else:
                    task = Task(
                        name="Gather more information",
                        description=(
                            "Ask targeted questions to better "
                            "understand the reported issue."
                        ),
                        required=True,
                    )

                plan = Plan(
                    goal_id=goal.id,
                    name="Investigate Reported Issue",
                    description=(
                        "Gather additional information to better "
                        "understand the reported issue."
                    ),
                    priority=goal.priority,
                    tasks=[task],
                )

                plans.setdefault(
                    goal.id,
                    plan,
                )
            elif goal.id.startswith("address_confirmed_"):
                plan = Plan(
                    goal_id=goal.id,
                    name=f"{goal.name} Plan",
                    description=(
                        "Confirm the extent of the issue and "
                        "recommend appropriate professional "
                        "treatment."
                    ),
                    priority=goal.priority,
                    tasks=[
                        Task(
                            name="Inspect property",
                            description=(
                                "Inspect the property to confirm "
                                "the extent of the issue."
                            ),
                        ),
                        Task(
                            name="Recommend treatment",
                            description=(
                                "Recommend appropriate professional "
                                "treatment to address the confirmed "
                                "issue."
                            ),
                        ),
                        Task(
                            name="Schedule follow-up",
                            description=(
                                "Schedule a follow-up to confirm "
                                "the issue has been resolved."
                            ),
                        ),
                    ],
                    constraints=[
                        Constraint(
                            name="Safety",
                            description=(
                                "Use appropriate PPE and follow "
                                "safe handling practices."
                            ),
                        )
                    ],
                )

                plans.setdefault(
                    goal.id,
                    plan,
                )

            elif self._requires_visual_evidence(goal):
                plan = Plan(
                    goal_id=goal.id,
                    name="Gather Visual Evidence",
                    description=(
                        "Gather visual evidence to better "
                        "understand the reported issue."
                    ),
                    priority=goal.priority,
                    tasks=[
                        Task(
                            name="Request Image Evidence",
                            description=(
                                "Request an image of the affected "
                                "area to gather visual evidence "
                                "and better understand the issue."
                            ),
                            
                            required=True,
                        ),
                    ],
                )

                plans.setdefault(
                    goal.id,
                    plan,
                )

        return list(plans.values())

    def _requires_visual_evidence(
        self,
        goal: Goal,
    ) -> bool:
        text = (
            f"{goal.name} "
            f"{goal.description}"
        ).lower()

        keywords = (
            "visual evidence",
            "image evidence",
            "photo evidence",
            "inspect image",
            "image",
            "photo",
            "picture",
        )

        return any(
            keyword in text
            for keyword in keywords
        )