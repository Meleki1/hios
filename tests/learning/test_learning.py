import pytest

from hios.capabilities.learning.models.lesson import Lesson
from hios.capabilities.learning.models.learning import Learning

from hios.capabilities.reflection.models.insight import Insight
from hios.capabilities.reflection.models.reflection import Reflection

from hios.capabilities.outcome.models.outcome import Outcome
from hios.capabilities.outcome.models.status import OutcomeStatus

from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.status import ExecutionStatus

from hios.capabilities.decision.models.decision import Decision
from hios.capabilities.planning.models.plan import Plan
from hios.capabilities.goals.models.priority import GoalPriority


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
                description="Inspection succeeded.",
            )
        ],
        summary="Execution successful.",
        score=1.0,
    )

def test_create_learning(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    assert learning.reflection == reflection

def test_default_lessons(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    assert learning.lessons == []

def test_add_lessons(
    reflection,
):

    learning = Learning(
        reflection=reflection,
        lessons=[
            Lesson(
                category="strategy",
                description="Inspect kitchens first.",
            )
        ],
    )

    assert len(learning.lessons) == 1

def test_default_summary(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    assert learning.summary == ""

def test_default_score(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    assert learning.score == 0.0

def test_serialization(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    dumped = learning.model_dump()

    assert dumped["score"] == 0.0

def test_copy(
    reflection,
):

    learning = Learning(
        reflection=reflection,
    )

    copied = learning.model_copy()

    assert copied == learning

def test_defaults_are_independent(
    reflection,
):

    learning1 = Learning(
        reflection=reflection,
    )

    learning2 = Learning(
        reflection=reflection,
    )

    learning1.lessons.append(
        Lesson(
            category="strategy",
            description="Inspect kitchens first.",
        )
    )

    assert learning2.lessons == []