from hios.capabilities.pest_control.models.observation import (
    PestObservation,
)

from hios.capabilities.pest_control.models.assessment import (
    PestAssessment,
)

from hios.capabilities.pest_control.models.recommendation import (
    PestRecommendation,
)

from hios.capabilities.pest_control.models.request import (
    PestControlRequest,
)


def test_pest_observation_can_be_created():

    observation = PestObservation(
        subject_id="subject-123",
        home_id="home-123",
        description=(
            "Small insects around the kitchen sink."
        ),
        location="kitchen",
    )

    assert observation.id is not None
    assert observation.subject_id == "subject-123"
    assert observation.home_id == "home-123"
    assert observation.pest_type is None
    assert observation.location == "kitchen"


def test_pest_assessment_can_be_created():

    assessment = PestAssessment(
        observation_id="observation-123",
        pest_type="ants",
        confidence=0.9,
        severity="low",
        explanation=(
            "The observed characteristics are "
            "consistent with ants."
        ),
    )

    assert assessment.id is not None
    assert assessment.observation_id == (
        "observation-123"
    )
    assert assessment.pest_type == "ants"
    assert assessment.confidence == 0.9


def test_pest_recommendation_can_be_created():

    recommendation = PestRecommendation(
        assessment_id="assessment-123",
        title="Inspect the affected area",
        description=(
            "Inspect the area for entry points "
            "and signs of activity."
        ),
        priority="normal",
        actions=[
            "Inspect entry points",
            "Monitor activity",
        ],
    )

    assert recommendation.id is not None
    assert recommendation.assessment_id == (
        "assessment-123"
    )
    assert len(recommendation.actions) == 2


def test_pest_control_request_can_be_created():

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message=(
            "I keep seeing insects around "
            "my kitchen."
        ),
    )

    assert request.subject_id == "subject-123"
    assert request.home_id == "home-123"
    assert request.message.startswith(
        "I keep seeing"
    )
    assert request.observation is None