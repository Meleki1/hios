import pytest

from hios.runtime.context import RuntimeContext

from hios.capabilities.decision.capability import DecisionCapability
from hios.capabilities.decision.contract import (
    DecisionRequest,
    DecisionResult,
)

from hios.capabilities.decision.default_capability import (
    DefaultDecisionCapability,
)

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.decision.selector import DecisionSelector

from hios.capabilities.goals.models.priority import GoalPriority

from hios.capabilities.planning.contract import PlanResult
from hios.capabilities.planning.models.plan import Plan

@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def plan():

    return Plan(
        goal_id="goal-1",
        name="Rodent Removal Plan",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )


@pytest.fixture
def plan_result(
    plan,
):

    return PlanResult(
        plans=[plan]
    )

class SpyDecisionSelector(
    DecisionSelector,
):

    def __init__(self):

        self.calls = 0

    def select(
        self,
        plans: PlanResult,
    ):

        self.calls += 1

        return None

class StubDecisionSelector(
    DecisionSelector,
):

    def select(
        self,
        plans: PlanResult,
    ):  
        if not plans.plans:
            return None

        return Decision(
            plan=plans.plans[0],
            rationale="Highest priority.",
            score=1.0,
        )

@pytest.mark.asyncio
async def test_returns_decision_result(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert isinstance(
        result,
        DecisionResult,
    )

@pytest.mark.asyncio
async def test_calls_selector_once(
    context,
    plan_result,
):

    selector = SpyDecisionSelector()

    capability = DefaultDecisionCapability(
        selector,
    )

    await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert selector.calls == 1

@pytest.mark.asyncio
async def test_returns_selected_decision(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert result.decision is not None

@pytest.mark.asyncio
async def test_empty_plan_result(
    context,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=PlanResult(),
        ),
        context,
    )

    assert result.decision is None

@pytest.mark.asyncio
async def test_preserves_selected_plan(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert (
        result.decision.plan.goal_id
        == "goal-1"
    )

@pytest.mark.asyncio
async def test_preserves_rationale(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert (
        result.decision.rationale
        == "Highest priority."
    )

@pytest.mark.asyncio
async def test_preserves_score(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    result = await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert result.decision.score == 1.0

@pytest.mark.asyncio
async def test_runtime_context_not_modified(
    context,
    plan_result,
):

    capability = DefaultDecisionCapability(
        StubDecisionSelector(),
    )

    before = context.model_copy()

    await capability.execute(
        DecisionRequest(
            plans=plan_result,
        ),
        context,
    )

    assert context == before

