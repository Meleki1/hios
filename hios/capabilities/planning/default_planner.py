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
            elif goal.name == "Eliminate infestation":
                plan = Plan(
                    goal_id=goal.id,
                    name="Rodent Elimination Plan",
                    description=(
                        "Eliminate the active rodent infestation."
                    ),
                    priority=goal.priority,
                    tasks=[
                        Task(
                            name="Inspect property",
                            description=(
                                "Inspect the property to locate "
                                "rodent activity."
                            ),
                            
                        ),
                        Task(
                            name="Seal entry points",
                            description=(
                                "Seal all identified entry points."
                            ),
                            
                        ),
                        Task(
                            name="Deploy traps",
                            description=(
                                "Place traps in strategic locations."
                            ),
                            
                        ),
                        Task(
                            name="Schedule follow-up",
                            description=(
                                "Schedule a follow-up inspection."
                            ),
                            
                        ),
                    ],
                    constraints=[
                        Constraint(
                            name="Safety",
                            description=(
                                "Use appropriate PPE while "
                                "handling rodents."
                            ),
                           
                        )
                    ],
                )

                plans.setdefault(
                    goal.id,
                    plan,
                )

            elif goal.name == "Prevent recurrence":
                plan = Plan(
                    goal_id=goal.id,
                    name="Rodent Prevention Plan",
                    description=(
                        "Reduce the likelihood of future infestations."
                    ),
                    priority=goal.priority,
                    tasks=[
                        Task(
                            name="Inspect property",
                            description=(
                                "Inspect for potential vulnerabilities."
                            ),
                            
                        ),
                        Task(
                            name="Educate customer",
                            description=(
                                "Provide prevention recommendations."
                            ),
                            
                        ),
                        Task(
                            name="Schedule monitoring",
                            description=(
                                "Arrange periodic inspections."
                            ),
                            
                        ),
                    ],
                    constraints=[
                        Constraint(
                            name="Customer Cooperation",
                            description=(
                                "Requires the customer to follow "
                                "prevention advice."
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