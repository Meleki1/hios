from openai import AsyncOpenAI

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.providers.image_diagnosis_provider import (
    ImageDiagnosisProvider,
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
            text_format=ImageDiagnosis,
        )

        return response.output_parsed

    @staticmethod
    def _encode_image(
        image: bytes,
    ) -> str:
        import base64

        return base64.b64encode(image).decode("utf-8")