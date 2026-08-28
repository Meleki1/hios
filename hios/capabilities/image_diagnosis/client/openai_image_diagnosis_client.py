from openai import AsyncOpenAI

from hios.core.config import get_settings
from hios.capabilities.image_diagnosis.providers.openai_image_diagnosis_provider import (
    OpenAIImageDiagnosisProvider,
)
from hios.capabilities.image_diagnosis.services.image_diagnosis_service import ImageDiagnosisService

settings = get_settings()

openai_client = AsyncOpenAI(
    api_key=settings.openai_api_key,
)

image_diagnosis_provider = OpenAIImageDiagnosisProvider(
    client=openai_client,
    model=settings.image_diagnosis_model,
)

image_diagnosis_service = ImageDiagnosisService(
    provider=image_diagnosis_provider,
)