import pytest

from hios.runtime.context import RuntimeContext

from hios.capabilities.learning.contract import (
    LearningRequest,
    LearningResult,
)
from hios.capabilities.learning.default_capability import (
    DefaultLearningCapability,
)
from hios.capabilities.learning.learner import Learner

from hios.capabilities.learning.models.learning import Learning
from hios.capabilities.learning.models.lesson import Lesson

from hios.capabilities.reflection.contract import ReflectionResult
from hios.capabilities.reflection.models.reflection import Reflection
from hios.capabilities.reflection.models.insight import Insight

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision

from hios.capabilities.planning.models.plan import Plan

from hios.capabilities.goals.models.priority import GoalPriority


@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def reflection():

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

    outcome = Outcome(
        execution=execution,
        status=OutcomeStatus.SUCCESS,
    )

    return Reflection(
        outcome=outcome,
        insights=[
            Insight(
                category="success",
                description="Inspection completed successfully.",
            )
        ],
        summary="Execution successful.",
        score=1.0,
    )


@pytest.fixture
def reflection_result(
    reflection,
):

    return ReflectionResult(
        reflection=reflection,
    )

class SpyLearner(
    Learner,
):

    def __init__(self):

        self.calls = 0

    def learn(
        self,
        reflection,
    ) -> Learning:

        self.calls += 1

        return Learning(
            reflection=reflection,
        )

class StubLearner(
    Learner,
):

    def learn(
        self,
        reflection,
    ) -> Learning:

        return Learning(
            reflection=reflection,
            lessons=[
                Lesson(
                    category="strategy",
                    description="Inspect kitchens first.",
                )
            ],
            summary="Useful strategy identified.",
            score=1.0,
        )

@pytest.mark.asyncio
async def test_returns_learning_result(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert isinstance(
        result,
        LearningResult,
    )

@pytest.mark.asyncio
async def test_calls_learner_once(
    context,
    reflection_result,
):

    learner = SpyLearner()

    capability = DefaultLearningCapability(
        learner,
    )

    await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert learner.calls == 1

@pytest.mark.asyncio
async def test_returns_generated_learning(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert result.learning is not None

@pytest.mark.asyncio
async def test_preserves_reflection(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert (
        result.learning.reflection
        == reflection_result.reflection
    )

@pytest.mark.asyncio
async def test_preserves_lessons(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert len(result.learning.lessons) == 1

    assert (
        result.learning.lessons[0].category
        == "strategy"
    )

@pytest.mark.asyncio
async def test_preserves_summary(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert (
        result.learning.summary
        == "Useful strategy identified."
    )

@pytest.mark.asyncio
async def test_preserves_score(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    result = await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert result.learning.score == 1.0


@pytest.mark.asyncio
async def test_runtime_context_not_modified(
    context,
    reflection_result,
):

    capability = DefaultLearningCapability(
        StubLearner(),
    )

    before = context.model_copy()

    await capability.execute(
        LearningRequest(
            reflection=reflection_result,
        ),
        context,
    )

    assert context == before


