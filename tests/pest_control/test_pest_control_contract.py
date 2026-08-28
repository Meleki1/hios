from hios.capabilities.pest_control.contract import (
    PestControlRequest,
    PestControlResult,
)

from hios.capabilities.pest_control.models.assessment import (
    PestAssessment,
)

from hios.capabilities.pest_control.models.recommendation import (
    PestRecommendation,
)


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


def test_pest_control_request_can_include_observation():

    request = PestControlRequest(
        subject_id="subject-123",
        home_id="home-123",
        message="I found something in my kitchen.",
        observation=(
            "Small insects observed around "
            "the kitchen sink."
        ),
    )

    assert request.observation is not None
    assert (
        "Small insects"
        in request.observation
    )


def test_pest_control_result_can_contain_assessment():

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

    result = PestControlResult(
        assessment=assessment,
    )

    assert result.assessment is not None
    assert (
        result.assessment.pest_type
        == "ants"
    )

    assert result.recommendations == []


def test_pest_control_result_can_contain_recommendations():

    recommendation = PestRecommendation(
        assessment_id="assessment-123",
        title="Inspect the affected area",
        description=(
            "Inspect the area for entry points."
        ),
        actions=[
            "Inspect entry points",
            "Monitor activity",
        ],
    )

    result = PestControlResult(
        recommendations=[
            recommendation,
        ],
    )

    assert len(result.recommendations) == 1

    assert (
        result.recommendations[0].title
        == "Inspect the affected area"
    )