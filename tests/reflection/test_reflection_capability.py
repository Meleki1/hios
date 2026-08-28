import pytest

from hios.runtime.context import RuntimeContext

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.models.plan import Plan

from hios.capabilities.outcome.contract import OutcomeResult
from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.reflection.contract import (
    ReflectionRequest,
    ReflectionResult,
)
from hios.capabilities.reflection.default_capability import (
    DefaultReflectionCapability,
)
from hios.capabilities.reflection.models.insight import Insight
from hios.capabilities.reflection.models.reflection import Reflection
from hios.capabilities.reflection.reflector import Reflector

@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def outcome():

    plan = Plan(
        goal_id="goal-1",
        name="Rodent Removal",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )

    decision = Decision(
        plan=plan,
        rationale="Highest priority.",
        score=1.0,
    )

    execution = Execution(
        decision=decision,
        status=ExecutionStatus.SUCCESS,
    )

    return Outcome(
        execution=execution,
        status=OutcomeStatus.SUCCESS,
    )


@pytest.fixture
def outcome_result(
    outcome,
):

    return OutcomeResult(
        outcome=outcome,
    )

class SpyReflector(
    Reflector,
):

    def __init__(self):

        self.calls = 0

    def reflect(
        self,
        outcome: Outcome,
    ) -> Reflection:

        self.calls += 1

        return Reflection(
            outcome=outcome,
        )

class StubReflector(
    Reflector,
):

    def reflect(
        self,
        outcome: Outcome,
    ) -> Reflection:

        return Reflection(
            outcome=outcome,
            insights=[
                Insight(
                    category="success",
                    description="Completed successfully.",
                )
            ],
            summary="Execution completed successfully.",
            score=1.0,
        )

@pytest.mark.asyncio
async def test_returns_reflection_result(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert isinstance(
        result,
        ReflectionResult,
    )

@pytest.mark.asyncio
async def test_calls_reflector_once(
    context,
    outcome_result,
):

    reflector = SpyReflector()

    capability = DefaultReflectionCapability(
        reflector,
    )

    await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert reflector.calls == 1

@pytest.mark.asyncio
async def test_returns_generated_reflection(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert result.reflection is not None

@pytest.mark.asyncio
async def test_preserves_outcome(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert (
        result.reflection.outcome
        == outcome_result.outcome
    )

@pytest.mark.asyncio
async def test_preserves_insights(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert len(result.reflection.insights) == 1

    assert (
        result.reflection.insights[0].category
        == "success"
    )

@pytest.mark.asyncio
async def test_preserves_summary(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert (
        result.reflection.summary
        == "Execution completed successfully."
    )

@pytest.mark.asyncio
async def test_preserves_score(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    result = await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert result.reflection.score == 1.0

@pytest.mark.asyncio
async def test_runtime_context_not_modified(
    context,
    outcome_result,
):

    capability = DefaultReflectionCapability(
        StubReflector(),
    )

    before = context.model_copy()

    await capability.execute(
        ReflectionRequest(
            outcome=outcome_result,
        ),
        context,
    )

    assert context == before