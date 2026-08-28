from abc import ABC, abstractmethod

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)


class ImageDiagnosisProvider(ABC):

    @abstractmethod
    async def diagnose(
        self,
        *,
        image: bytes,
    ) -> ImageDiagnosis:
        ...