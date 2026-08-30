import pytest

from hios.runtime.context import RuntimeContext

from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.goals.models.priority import GoalPriority

from hios.capabilities.planning.contract import (
    PlanRequest,
    PlanResult,
)

from hios.capabilities.planning.default_capability import (
    DefaultPlanningCapability,
)

from hios.capabilities.planning.default_planner import (
    DefaultPlanner,
)

from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.planning.planner import Planner

@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def goal_result():

    return GoalResult(
        goals=[
            Goal(
                id="rodent",
                name="Eliminate infestation",
                description="Remove rodents.",
                priority=GoalPriority.CRITICAL,
            )
        ]
    )

class SpyPlanner(Planner):

    def __init__(self):

        self.calls = 0
        self.investigation_question = None

    def create(
        self,
        goals: GoalResult,
        investigation_question=None,
    ) -> list[Plan]:

        self.calls += 1
        self.investigation_question = investigation_question

        return []


@pytest.mark.asyncio
async def test_returns_plan_result(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert isinstance(
        result,
        PlanResult,
    )

@pytest.mark.asyncio
async def test_calls_planner_once(
    context,
    goal_result,
):

    planner = SpyPlanner()

    capability = DefaultPlanningCapability(
        planner,
    )

    await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert planner.calls == 1

@pytest.mark.asyncio
async def test_returns_generated_plans(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert len(result.plans) == 1

@pytest.mark.asyncio
async def test_empty_goal_result(
    context,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=GoalResult(),
        ),
        context,
    )

    assert result.plans == []

@pytest.mark.asyncio
async def test_preserves_plan_order(
    context,
):

    goals = GoalResult(
        goals=[
            Goal(
                id="1",
                name="Eliminate infestation",
                description="",
                priority=GoalPriority.CRITICAL,
            ),
            Goal(
                id="2",
                name="Prevent recurrence",
                description="",
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goals,
        ),
        context,
    )

    assert result.plans[0].goal_id == "1"
    assert result.plans[1].goal_id == "2"

@pytest.mark.asyncio
async def test_multiple_plans(
    context,
):

    goals = GoalResult(
        goals=[
            Goal(
                id="1",
                name="Eliminate infestation",
                description="",
                priority=GoalPriority.CRITICAL,
            ),
            Goal(
                id="2",
                name="Prevent recurrence",
                description="",
                priority=GoalPriority.HIGH,
            ),
        ]
    )

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goals,
        ),
        context,
    )

    assert len(result.plans) == 2

@pytest.mark.asyncio
async def test_priority_preserved(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert (
        result.plans[0].priority
        == GoalPriority.CRITICAL
    )


@pytest.mark.asyncio
async def test_tasks_preserved(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert len(
        result.plans[0].tasks
    ) == 4

@pytest.mark.asyncio
async def test_constraints_preserved(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )

    assert len(
        result.plans[0].constraints
    ) == 1

@pytest.mark.asyncio
async def test_generated_plan_ids_preserved(
    context,
    goal_result,
):

    capability = DefaultPlanningCapability(
        DefaultPlanner(),
    )

    result = await capability.execute(
        PlanRequest(
            goals=goal_result,
        ),
        context,
    )
    

    assert result.plans[0].id != ""