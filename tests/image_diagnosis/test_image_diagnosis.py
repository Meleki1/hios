import pytest
from pydantic import ValidationError

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)


def test_image_diagnosis_can_contain_findings():

    finding = ImageFinding(
        category="pest",
        description=(
            "Possible rodent evidence detected."
        ),
        confidence=0.91,
        location="kitchen",
    )

    diagnosis = ImageDiagnosis(
        findings=[finding],
        overall_confidence=0.91,
    )

    assert diagnosis.findings == [finding]
    assert diagnosis.overall_confidence == 0.91


def test_image_diagnosis_allows_no_findings():

    diagnosis = ImageDiagnosis(
        overall_confidence=0.2,
    )

    assert diagnosis.findings == []


def test_image_diagnosis_defaults_metadata_to_empty_dict():

    diagnosis = ImageDiagnosis(
        overall_confidence=0.5,
    )

    assert diagnosis.metadata == {}


def test_image_diagnosis_preserves_multiple_findings():

    findings = [
        ImageFinding(
            category="pest",
            description="Possible rodent evidence.",
            confidence=0.91,
            location="kitchen",
        ),
        ImageFinding(
            category="property_damage",
            description="Possible damage near cabinet.",
            confidence=0.76,
            location="kitchen",
        ),
    ]

    diagnosis = ImageDiagnosis(
        findings=findings,
        overall_confidence=0.84,
    )

    assert len(diagnosis.findings) == 2
    assert diagnosis.findings[0].category == "pest"
    assert (
        diagnosis.findings[1].category
        == "property_damage"
    )


@pytest.mark.parametrize(
    "confidence",
    [-0.01, 1.01],
)
def test_image_diagnosis_rejects_invalid_overall_confidence(
    confidence,
):

    with pytest.raises(ValidationError):
        ImageDiagnosis(
            overall_confidence=confidence,
        )