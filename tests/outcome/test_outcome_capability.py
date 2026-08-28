import pytest

from hios.runtime.context import RuntimeContext

from hios.capabilities.execution.contract import ExecutionResult
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.models.plan import Plan

from hios.capabilities.outcome.contract import OutcomeCapability
from hios.capabilities.outcome.contract import (
    OutcomeRequest,
    OutcomeResult,
)
from hios.capabilities.outcome.default_capability import (
    DefaultOutcomeCapability,
)
from hios.capabilities.outcome.evaluator import OutcomeEvaluator
from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def execution():

    plan = Plan(
        goal_id="goal-1",
        name="Rodent Plan",
        description="Remove rodents.",
        priority=GoalPriority.CRITICAL,
    )

    decision = Decision(
        plan=plan,
        rationale="Highest priority.",
        score=1.0,
    )

    return Execution(
        decision=decision,
        status=ExecutionStatus.SUCCESS,
    )


@pytest.fixture
def execution_result(
    execution,
):

    return ExecutionResult(
        execution=execution,
    )

class SpyOutcomeEvaluator(
    OutcomeEvaluator,
):

    def __init__(self):

        self.calls = 0

    def evaluate(
        self,
        execution: Execution,
    ) -> Outcome:

        self.calls += 1

        return Outcome(
            execution=execution,
            status=OutcomeStatus.SUCCESS,
        )

class StubOutcomeEvaluator(
    OutcomeEvaluator,
):

    def evaluate(
        self,
        execution: Execution,
    ) -> Outcome:

        return Outcome(
            execution=execution,
            status=OutcomeStatus.SUCCESS,
        )

@pytest.mark.asyncio
async def test_returns_outcome_result(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert isinstance(
        result,
        OutcomeResult,
    )

@pytest.mark.asyncio
async def test_calls_evaluator_once(
    context,
    execution_result,
):

    evaluator = SpyOutcomeEvaluator()

    capability = DefaultOutcomeCapability(
        evaluator,
    )

    await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert evaluator.calls == 1

@pytest.mark.asyncio
async def test_returns_generated_outcome(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert result.outcome is not None

@pytest.mark.asyncio
async def test_preserves_execution(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert (
        result.outcome.execution
        == execution_result.execution
    )

@pytest.mark.asyncio
async def test_preserves_status(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert (
        result.outcome.status
        == OutcomeStatus.SUCCESS
    )

@pytest.mark.asyncio
async def test_preserves_observations(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert result.outcome.observations == []

@pytest.mark.asyncio
async def test_preserves_summary(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    result = await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert result.outcome.summary == ""

@pytest.mark.asyncio
async def test_runtime_context_not_modified(
    context,
    execution_result,
):

    capability = DefaultOutcomeCapability(
        StubOutcomeEvaluator(),
    )

    before = context.model_copy()

    await capability.execute(
        OutcomeRequest(
            execution=execution_result,
        ),
        context,
    )

    assert context == before

