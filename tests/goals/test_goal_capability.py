import pytest

from hios.capabilities.goals.capability import GoalCapability
from hios.capabilities.goals.contract.result import GoalResult
from hios.capabilities.goals.capability import DefaultGoalCapability

from hios.capabilities.goals.request import GoalRequest
from hios.capabilities.goals.default import DefaultGoalGenerator
from hios.capabilities.goals.models.goal import Goal
from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)
from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
)
from hios.runtime.context import RuntimeContext

class SpyGoalGenerator(DefaultGoalGenerator):

    def __init__(self):

        super().__init__()

        self.calls = 0

    def generate(
        self,
        understanding,
    ):

        self.calls += 1

        return super().generate(
            understanding,
        )

@pytest.fixture
def context():

    return RuntimeContext()


@pytest.fixture
def understanding():

    return UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="rodent",
                name="Rodent Infestation",
                description="Evidence suggests rodents.",
                confidence=0.9,
                supporting_facts=[
                    "Possible rodent activity",
                ],
                evidence=[],
            )
        ]
    )


@pytest.mark.asyncio
async def test_goal_capability_returns_goal_result(
    context,
    understanding,
):


    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    assert isinstance(
        result,
        GoalResult,
    )

@pytest.mark.asyncio
async def test_goal_capability_calls_generator_once(
    context,
    understanding,
):

    generator = SpyGoalGenerator()

    capability = DefaultGoalCapability(
        generator,
    )

    await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    assert generator.calls == 1

@pytest.mark.asyncio
async def test_goal_capability_returns_generated_goals(
    context,
    understanding,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    assert len(result.goals) == 2

    assert result.goals[0].name == "Eliminate infestation"

    assert result.goals[1].name == "Prevent recurrence"

@pytest.mark.asyncio
async def test_goal_capability_empty_understanding(
    context,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=UnderstandingResult(),
        ),
        context,
    )

    assert result.goals == []

@pytest.mark.asyncio
async def test_goal_capability_preserves_goal_order(
    context,
    understanding,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    priorities = [
        goal.priority.value
        for goal in result.goals
    ]

    assert priorities == [
        "critical",
        "high",
    ]

@pytest.mark.asyncio
async def test_goal_capability_multiple_goals(
    context,
    understanding,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    assert len(result.goals) >= 2

@pytest.mark.asyncio
async def test_goal_capability_preserves_goal_ids(
    context,
    understanding,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    ids = {
        goal.id
        for goal in result.goals
    }

    assert len(ids) == len(result.goals)

@pytest.mark.asyncio
async def test_goal_capability_preserves_source_hypothesis(
    context,
    understanding,
):

    capability = DefaultGoalCapability(
        DefaultGoalGenerator(),
    )

    result = await capability.execute(
        GoalRequest(
            understanding=understanding,
        ),
        context,
    )

    for goal in result.goals:

        assert goal.source_hypothesis == "rodent"

