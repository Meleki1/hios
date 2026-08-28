from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.providers.image_diagnosis_provider import (
    ImageDiagnosisProvider,
)


class ImageDiagnosisService:

    def __init__(
        self,
        *,
        provider: ImageDiagnosisProvider,
    ):
        self.provider = provider

    async def diagnose(
        self,
        *,
        image: bytes,
    ) -> ImageDiagnosis:

        return await self.provider.diagnose(
            image=image,
        )