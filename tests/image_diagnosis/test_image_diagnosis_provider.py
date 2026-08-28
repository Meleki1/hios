from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from tests.image_diagnosis.fakes import (
    FakeImageDiagnosisProvider,
)


async def test_provider_returns_image_diagnosis():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description=(
                    "Possible rodent evidence."
                ),
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    provider = FakeImageDiagnosisProvider(
        diagnosis=diagnosis,
    )

    result = await provider.diagnose(
        image=b"fake-image-data",
    )

    assert result is diagnosis


async def test_provider_receives_image_bytes():

    provider = FakeImageDiagnosisProvider()

    image = b"fake-image-data"

    await provider.diagnose(
        image=image,
    )

    assert len(provider.calls) == 1
    assert provider.calls[0]["image"] == image