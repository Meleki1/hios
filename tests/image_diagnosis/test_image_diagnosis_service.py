import pytest

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.services.image_diagnosis_service import (
    ImageDiagnosisService,
)
from tests.image_diagnosis.fakes import (
    FakeImageDiagnosisProvider, FailingImageDiagnosisProvider
)


@pytest.mark.asyncio
async def test_image_diagnosis_service_uses_provider():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    service = ImageDiagnosisService(
        provider=provider,
    )

    image = b"fake-image-data"

    result = await service.diagnose(
        image=image,
    )

    assert result is diagnosis

    assert len(provider.calls) == 1
    assert provider.calls[0]["image"] == image

@pytest.mark.asyncio
async def test_image_diagnosis_service_uses_provider():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    service = ImageDiagnosisService(
        provider=provider,
    )

    image = b"fake-image-data"

    result = await service.diagnose(
        image=image,
    )

    assert result is diagnosis
    assert len(provider.calls) == 1
    assert provider.calls[0]["image"] == image

@pytest.mark.asyncio
async def test_image_diagnosis_service_propagates_provider_error():

    provider = FailingImageDiagnosisProvider()

    service = ImageDiagnosisService(
        provider=provider,
    )

    with pytest.raises(
        RuntimeError,
        match="Image diagnosis provider failed.",
    ):
        await service.diagnose(
            image=b"fake-image-data",
        )

@pytest.mark.asyncio
async def test_image_diagnosis_service_accepts_empty_diagnosis():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    service = ImageDiagnosisService(
        provider=provider,
    )

    result = await service.diagnose(
        image=b"fake-image-data",
    )

    assert result is diagnosis
    assert result.findings == []
    assert result.overall_confidence == 0.0

def test_image_finding_rejects_confidence_above_one():

    with pytest.raises(ValueError):
        ImageFinding(
            category="pest",
            description="Possible pest evidence.",
            confidence=1.1,
        )


def test_image_finding_rejects_negative_confidence():

    with pytest.raises(ValueError):
        ImageFinding(
            category="pest",
            description="Possible pest evidence.",
            confidence=-0.1,
        )


def test_image_finding_allows_missing_location():

    finding = ImageFinding(
        category="pest",
        description="Possible pest evidence.",
        confidence=0.8,
    )

    assert finding.location is None


def test_image_diagnosis_rejects_confidence_above_one():

    with pytest.raises(ValueError):
        ImageDiagnosis(
            findings=[],
            overall_confidence=1.1,
        )


def test_image_diagnosis_rejects_negative_confidence():

    with pytest.raises(ValueError):
        ImageDiagnosis(
            findings=[],
            overall_confidence=-0.1,
        )


def test_image_diagnosis_defaults_to_empty_findings():

    diagnosis = ImageDiagnosis(
        overall_confidence=0.0,
    )

    assert diagnosis.findings == []


def test_image_diagnosis_defaults_to_empty_metadata():

    diagnosis = ImageDiagnosis(
        overall_confidence=0.0,
    )

    assert diagnosis.metadata == {}

@pytest.mark.asyncio
async def test_provider_returns_valid_image_diagnosis():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            )
        ],
        overall_confidence=0.91,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    result = await provider.diagnose(
        image=b"fake-image-data",
    )

    assert isinstance(result, ImageDiagnosis)
    assert len(result.findings) == 1

    finding = result.findings[0]

    assert isinstance(finding, ImageFinding)
    assert finding.category == "pest"
    assert finding.description == "Possible rodent evidence."
    assert finding.confidence == 0.91
    assert finding.location == "kitchen"

@pytest.mark.asyncio
async def test_provider_preserves_multiple_findings():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
            ImageFinding(
                category="entry_point",
                description="Possible opening beneath the cabinet.",
                confidence=0.78,
                location="kitchen",
            ),
        ],
        overall_confidence=0.86,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    result = await provider.diagnose(
        image=b"fake-image-data",
    )

    assert len(result.findings) == 2
    assert result.findings[0].category == "pest"
    assert result.findings[1].category == "entry_point"

@pytest.mark.asyncio
async def test_provider_can_return_no_findings():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    result = await provider.diagnose(
        image=b"fake-image-data",
    )

    assert isinstance(result, ImageDiagnosis)
    assert result.findings == []
    assert result.overall_confidence == 0.0

@pytest.mark.asyncio
async def test_provider_preserves_diagnosis_metadata():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.9,
            )
        ],
        overall_confidence=0.9,
        metadata={
            "analysis_type": "pest_detection",
        },
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    result = await provider.diagnose(
        image=b"fake-image-data",
    )

    assert result.metadata["analysis_type"] == "pest_detection"

@pytest.mark.asyncio
async def test_image_diagnosis_service_uses_provider():
    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    service = ImageDiagnosisService(
        provider=provider,
    )

    image = b"fake-image-data"

    result = await service.diagnose(
        image=image,
    )

    assert result == diagnosis

    assert len(provider.calls) == 1

    assert provider.calls[0]["image"] == image