import pytest

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.models.plan import Plan


@pytest.fixture
def plan():

    return Plan(
        goal_id="goal-1",
        name="Rodent Removal Plan",
        description="Remove rodents from the property.",
        priority=GoalPriority.CRITICAL,
    )

def test_create_decision(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Highest priority plan.",
        score=0.95,
    )

    assert decision.plan == plan
    assert decision.score == 0.95

def test_decision_stores_rationale(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Selected because of urgency.",
        score=1.0,
    )

    assert decision.rationale == "Selected because of urgency."

def test_decision_contains_selected_plan(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Best option.",
        score=0.9,
    )

    assert decision.plan.goal_id == "goal-1"

def test_decision_score():

    decision = Decision(
        plan=Plan(
            goal_id="goal",
            name="Plan",
            description="Description",
            priority=GoalPriority.HIGH,
        ),
        rationale="Good choice.",
        score=0.75,
    )

    assert decision.score == 0.75

def test_decision_serialization(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Chosen.",
        score=0.9,
    )

    dumped = decision.model_dump()

    assert dumped["score"] == 0.9
    assert dumped["rationale"] == "Chosen."

def test_decision_copy(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Chosen.",
        score=0.9,
    )

    copied = decision.model_copy()

    assert copied == decision

def test_decision_equality(
    plan,
):

    decision = Decision(
        plan=plan,
        rationale="Chosen.",
        score=0.9,
    )

    copied = decision.model_copy()

    assert copied == decision