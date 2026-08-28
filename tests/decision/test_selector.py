import pytest

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.decision.default import DefaultDecisionSelector
from hios.capabilities.goals.models.priority import GoalPriority
from hios.capabilities.planning.contract import PlanResult
from hios.capabilities.planning.models.plan import Plan

@pytest.fixture
def selector():

    return DefaultDecisionSelector()


@pytest.fixture
def critical_plan():

    return Plan(
        goal_id="goal-1",
        name="Critical Plan",
        description="Highest priority.",
        priority=GoalPriority.CRITICAL,
    )


@pytest.fixture
def high_plan():

    return Plan(
        goal_id="goal-2",
        name="High Plan",
        description="High priority.",
        priority=GoalPriority.HIGH,
    )


@pytest.fixture
def medium_plan():

    return Plan(
        goal_id="goal-3",
        name="Medium Plan",
        description="Medium priority.",
        priority=GoalPriority.MEDIUM,
    )

def test_empty_plan_result(selector):

    decision = selector.select(
        PlanResult()
    )

    assert decision is None

def test_single_plan_selected(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[critical_plan]
        )
    )

    assert decision.plan == critical_plan

def test_returns_decision(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[critical_plan]
        )
    )

    assert isinstance(
        decision,
        Decision,
    )

def test_highest_priority_selected(
    selector,
    critical_plan,
    medium_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[
                medium_plan,
                critical_plan,
            ]
        )
    )

    assert (
        decision.plan.priority
        == GoalPriority.CRITICAL
    )

def test_selected_plan_preserved(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[critical_plan]
        )
    )

    assert (
        decision.plan.goal_id
        == critical_plan.goal_id
    )

def test_decision_contains_rationale(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[critical_plan]
        )
    )

    assert decision.rationale != ""


def test_decision_score(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[critical_plan]
        )
    )

    assert decision.score == 1.0

def test_selection_is_deterministic(
    selector,
    critical_plan,
    high_plan,
):

    plans = PlanResult(
        plans=[
            critical_plan,
            high_plan,
        ]
    )

    first = selector.select(plans)
    second = selector.select(plans)

    assert first == second

def test_duplicate_plans(
    selector,
    critical_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[
                critical_plan,
                critical_plan,
            ]
        )
    )

    assert decision.plan == critical_plan

def test_priority_ordering(
    selector,
    critical_plan,
    high_plan,
    medium_plan,
):

    decision = selector.select(
        PlanResult(
            plans=[
                medium_plan,
                high_plan,
                critical_plan,
            ]
        )
    )

    assert (
        decision.plan.priority
        == GoalPriority.CRITICAL
    )