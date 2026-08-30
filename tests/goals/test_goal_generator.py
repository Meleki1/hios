import pytest

from hios.capabilities.goals.default import (
    DefaultGoalGenerator,
)

from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)

from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
)
from hios.capabilities.understanding.models.unknown import Unknown


@pytest.fixture
def generator():

    return DefaultGoalGenerator()


@pytest.fixture
def rodent_hypothesis():

    return Hypothesis(
        id="rodent",
        name="Rodent Infestation",
        description="Evidence suggests rodents are present.",
        confidence=0.9,
        supporting_facts=[
            "Possible rodent activity",
        ],
        evidence=[],
    )


@pytest.fixture
def cockroach_hypothesis():

    return Hypothesis(
        id="cockroach",
        name="Cockroach Infestation",
        description="Evidence suggests cockroaches are present.",
        confidence=0.8,
        supporting_facts=[
            "Cockroach droppings",
        ],
        evidence=[],
    )

def test_empty_understanding_returns_no_goals(generator):

    understanding = UnderstandingResult()

    goals = generator.generate(
        understanding,
    )

    assert goals == []

def test_generate_goals_from_rodent_hypothesis(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert len(goals) == 2

    assert goals[0].name == "Eliminate infestation"

    assert goals[1].name == "Prevent recurrence"

def test_goal_priority(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert goals[0].priority.value == "critical"

    assert goals[1].priority.value == "high"

def test_goal_tracks_source_hypothesis(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    for goal in goals:

        assert goal.source_hypothesis == "rodent"

def test_unknown_hypothesis_generates_no_goals(
    generator,
):

    understanding = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="bird",
                name="Bird Activity",
                description="Birds may be nesting.",
                confidence=0.6,
                supporting_facts=[],
                evidence=[],
            )
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert goals == []

def test_multiple_hypotheses(
    generator,
    rodent_hypothesis,
    cockroach_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
            cockroach_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert len(goals) >= 2

def test_duplicate_hypotheses_do_not_duplicate_goals(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    names = [goal.name for goal in goals]

    assert len(names) == len(set(names))

def test_goal_order(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert goals[0].priority.value == "critical"

    assert goals[1].priority.value == "high"

def test_generated_goals_have_ids(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    for goal in goals:

        assert goal.id is not None

        assert goal.id != ""

def test_generated_goals_are_pending(
    generator,
    rodent_hypothesis,
):

    understanding = UnderstandingResult(
        hypotheses=[
            rodent_hypothesis,
        ]
    )

    goals = generator.generate(
        understanding,
    )

    for goal in goals:

        assert goal.status.value == "pending"

def test_generate_evidence_goal_from_possible_rodent_activity(
    generator,
):
    understanding = UnderstandingResult(
        hypotheses=[
            Hypothesis(
                id="rodent",
                name="Possible Rodent Activity",
                description=(
                    "Evidence suggests possible rodent activity."
                ),
                confidence=0.7,
                supporting_facts=[
                    "Possible rodent activity",
                ],
                evidence=[],
            )
        ]
    )

    goals = generator.generate(
        understanding,
    )

    assert len(goals) == 1

    goal = goals[0]

    assert goal.id == "investigate_rodent_activity"
    assert goal.name == "Gather visual evidence"
    assert goal.priority.value == "high"
    assert goal.source_hypothesis == "rodent"
    assert goal.status.value == "pending"

def test_generate_investigation_goal_from_unknown(
    generator,
):
    understanding = UnderstandingResult(
        hypotheses=[],
        unknowns=[
            Unknown(
                description=(
                    "The nature and source of the "
                    "reported issue are not yet clear."
                )
            )
        ],
    )

    goals = generator.generate(
        understanding,
    )

    assert len(goals) == 1

    goal = goals[0]

    assert goal.id == "investigate_issue"
    assert goal.name == "Understand the reported issue"
    assert goal.priority.value == "high"
    assert goal.source_hypothesis is None