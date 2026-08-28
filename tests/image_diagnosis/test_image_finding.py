import pytest
from pydantic import ValidationError

from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)


def test_image_finding_can_be_created():

    finding = ImageFinding(
        category="pest",
        description=(
            "Possible rodent evidence detected."
        ),
        confidence=0.91,
        location="kitchen",
    )

    assert finding.category == "pest"
    assert finding.description == (
        "Possible rodent evidence detected."
    )
    assert finding.confidence == 0.91
    assert finding.location == "kitchen"


def test_image_finding_allows_missing_location():

    finding = ImageFinding(
        category="pest",
        description="Possible pest evidence.",
        confidence=0.8,
    )

    assert finding.location is None


def test_image_finding_defaults_metadata_to_empty_dict():

    finding = ImageFinding(
        category="pest",
        description="Possible pest evidence.",
        confidence=0.8,
    )

    assert finding.metadata == {}


@pytest.mark.parametrize(
    "confidence",
    [-0.01, 1.01],
)
def test_image_finding_rejects_invalid_confidence(
    confidence,
):

    with pytest.raises(ValidationError):
        ImageFinding(
            category="pest",
            description="Possible pest evidence.",
            confidence=confidence,
        )


def test_image_finding_preserves_metadata():

    finding = ImageFinding(
        category="pest",
        description="Possible rodent evidence.",
        confidence=0.91,
        location="kitchen",
        metadata={
            "visual_features": [
                "small droppings",
                "possible gnaw marks",
            ],
        },
    )

    assert finding.metadata == {
        "visual_features": [
            "small droppings",
            "possible gnaw marks",
        ],
    }