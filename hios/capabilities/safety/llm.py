import re
from hios.capabilities.assistant.llm.contract import AssistantLLM
from hios.capabilities.understanding.contract import (
    UnderstandingResult,
)


_SYSTEM_PROMPT = (
    "You are the safety-guidance module of a home-services "
    "assistant. Your only job is to give short, practical safety "
    "precautions relevant to whatever pest activity is currently "
    "suspected -- nothing else.\n\n"
    "Strict rules:\n"
    "- Base your guidance only on the specific pest(s) named "
    "below. Never mention a pest that is not named.\n"
    "- If no specific pest has been identified yet, give general "
    "precautions appropriate for an unidentified pest issue.\n"
    "- Output between 2 and 4 short, imperative precautions.\n"
    "- Do not ask questions.\n"
    "- Do not request a photo or any other information from the "
    "user.\n"
    "- Do not describe next steps, diagnosis, or what will happen "
    "next.\n"
    "- Do not add greetings, sign-offs, or explanations.\n"
    "- Output exactly one precaution per line, with no bullets, "
    "numbers, or extra punctuation at the start of the line."
)

_FALLBACK_GUIDANCE = [
    (
        "Avoid direct contact with any suspected pests, "
        "droppings, or contaminated material until the "
        "situation is better understood."
    ),
    (
        "Keep children and pets away from the affected area "
        "as a precaution."
    ),
]


class LLMSafetyGuidanceGenerator:

    def __init__(
        self,
        *,
        llm: AssistantLLM,
    ) -> None:
        self._llm = llm

    async def generate(
        self,
        understanding: UnderstandingResult,
    ) -> list[str]:

        user_prompt = self._build_user_prompt(understanding)

        try:
            response = await self._llm.generate(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )
        except Exception:
            return list(_FALLBACK_GUIDANCE)

        guidance = self._parse(response)

        if not guidance:
            return list(_FALLBACK_GUIDANCE)

        return guidance

    def _build_user_prompt(
        self,
        understanding: UnderstandingResult,
    ) -> str:

        if not understanding.hypotheses:
            return (
                "No specific pest has been identified yet. "
                "Provide general safety precautions for a "
                "possible, unidentified pest issue."
            )

        lines = [
            "Suspected pest activity, most likely first:",
        ]

        for hypothesis in understanding.hypotheses:
            lines.append(
                f"- {hypothesis.name} "
                f"(confidence: {hypothesis.confidence:.2f}): "
                f"{hypothesis.description}"
            )

        lines.append(
            "\nProvide safety precautions relevant to this "
            "activity."
        )

        return "\n".join(lines)

    def _parse(
        self,
        response: str,
    ) -> list[str]:

        lines = [
            self._strip_leading_marker(line).strip()
            for line in response.strip().splitlines()
        ]

        guidance = [line for line in lines if line]

        return list(dict.fromkeys(guidance))

    @staticmethod
    def _strip_leading_marker(
        line: str,
    ) -> str:
        return re.sub(
            r"^\s*(?:[-•*]|\d+[.)])\s*",
            "",
            line,
        )
