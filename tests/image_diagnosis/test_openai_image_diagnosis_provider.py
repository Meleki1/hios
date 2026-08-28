from types import SimpleNamespace
from openai import AsyncOpenAI
import pytest

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.providers.openai_image_diagnosis_provider import (
    OpenAIImageDiagnosisProvider,
)
from hios.capabilities.image_diagnosis.services.image_diagnosis_service import (
    ImageDiagnosisService,
)


class FakeResponses:

    def __init__(
        self,
        diagnosis: ImageDiagnosis,
    ):
        self.diagnosis = diagnosis
        self.calls = []

    async def parse(
        self,
        **kwargs,
    ):
        self.calls.append(kwargs)

        return SimpleNamespace(
            output_parsed=self.diagnosis,
        )


class FakeOpenAIClient:

    def __init__(
        self,
        diagnosis: ImageDiagnosis,
    ):
        self.responses = FakeResponses(
            diagnosis,
        )


@pytest.mark.asyncio
async def test_provider_returns_image_diagnosis():

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

    client = FakeOpenAIClient(
        diagnosis,
    )

    provider = OpenAIImageDiagnosisProvider(
        client=client,
        model="gpt-4o-mini",
    )

    image = b"fake-image-data"

    result = await provider.diagnose(
        image=image,
    )

    assert result is diagnosis

@pytest.mark.asyncio
async def test_provider_sends_image_to_openai():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    client = FakeOpenAIClient(
        diagnosis,
    )

    provider = OpenAIImageDiagnosisProvider(
        client=client,
        model="gpt-4o-mini",
    )

    image = b"fake-image-data"

    await provider.diagnose(
        image=image,
    )

    call = client.responses.calls[0]

    content = call["input"][0]["content"]

    image_content = content[1]

    assert image_content["type"] == "input_image"
    assert image_content["image_url"].startswith(
        "data:image/jpeg;base64,"
    )

@pytest.mark.asyncio
async def test_provider_uses_configured_model():

    diagnosis = ImageDiagnosis(
        findings=[],
        overall_confidence=0.0,
    )

    client = FakeOpenAIClient(
        diagnosis,
    )

    provider = OpenAIImageDiagnosisProvider(
        client=client,
        model="test-vision-model",
    )

    await provider.diagnose(
        image=b"fake-image",
    )

    call = client.responses.calls[0]

    assert call["model"] == "test-vision-model"

def test_image_diagnosis_service_is_wired():
    client = AsyncOpenAI(
        api_key="test-key",
    )

    provider = OpenAIImageDiagnosisProvider(
        client=client,
        model="gpt-4o-mini",
    )

    service = ImageDiagnosisService(
        provider=provider,
    )

    assert service.provider is provider