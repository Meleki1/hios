from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.providers.image_diagnosis_provider import (
    ImageDiagnosisProvider,
)


class _ImageFindingResponse(BaseModel):
    category: str
    description: str

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )

    location: str | None = None


class _ImageDiagnosisResponse(BaseModel):
   

    findings: list[_ImageFindingResponse] = Field(
        default_factory=list,
    )

    overall_confidence: float = Field(
        ge=0.0,
        le=1.0,
    )


class OpenAIImageDiagnosisProvider(
    ImageDiagnosisProvider
):

    def __init__(
        self,
        *,
        client: AsyncOpenAI,
        model: str,
    ):
        self._client = client
        self._model = model

    async def diagnose(
        self,
        *,
        image: bytes,
    ) -> ImageDiagnosis:

        response = await self._client.responses.parse(
            model=self._model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Analyze this image to identify "
                                "visible evidence relevant to "
                                "the reported issue. "
                                "Return only observations that "
                                "can reasonably be supported "
                                "by the image."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                "data:image/jpeg;base64,"
                                + self._encode_image(image)
                            ),
                        },
                    ],
                }
            ],
            text_format=_ImageDiagnosisResponse,
        )

        parsed = response.output_parsed

        return ImageDiagnosis(
            findings=[
                ImageFinding(
                    category=finding.category,
                    description=finding.description,
                    confidence=finding.confidence,
                    location=finding.location,
                )
                for finding in parsed.findings
            ],
            overall_confidence=parsed.overall_confidence,
        )

    @staticmethod
    def _encode_image(
        image: bytes,
    ) -> str:
        import base64

        return base64.b64encode(image).decode("utf-8")