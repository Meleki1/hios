from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.providers.image_diagnosis_provider import (
    ImageDiagnosisProvider,
)


class FakeImageDiagnosisProvider(
    ImageDiagnosisProvider,
):

    def __init__(
        self,
        *,
        diagnosis: ImageDiagnosis | None = None,
    ):
        self.diagnosis = diagnosis
        self.calls: list[dict] = []

    async def diagnose(
        self,
        *,
        image: bytes,
    ) -> ImageDiagnosis:

        self.calls.append(
            {
                "image": image,
            }
        )

        if self.diagnosis is not None:
            return self.diagnosis

        return ImageDiagnosis(
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

class FailingImageDiagnosisProvider(ImageDiagnosisProvider):

    async def diagnose(
        self,
        *,
        image: bytes,
    ) -> ImageDiagnosis:
        raise RuntimeError(
            "Image diagnosis provider failed."
        )
