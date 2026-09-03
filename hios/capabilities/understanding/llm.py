import json

from hios.capabilities.assistant.llm.contract import AssistantLLM
from hios.capabilities.understanding.contract import (
    UnderstandingRequest,
    UnderstandingResult,
)
from hios.capabilities.understanding.models.hypothesis import (
    Hypothesis,
    HypothesisStatus,
)
from hios.capabilities.understanding.models.unknown import Unknown
from hios.capabilities.understanding.strategy import UnderstandingStrategy


_SYSTEM_PROMPT = (
    "You are the pest-identification reasoning module for a "
    "home-services assistant that covers a wide and growing range "
    "of pests -- rodents, cockroaches, ants, termites, bed bugs, "
    "wasps and other stinging insects, spiders, fleas, ticks, "
    "silverfish, and many others. You are not limited to a fixed "
    "list -- use your own knowledge of pest signs and behavior.\n\n"
    "Given a homeowner's report and, when present, a description "
    "of photographic evidence, identify which pest(s), if any, "
    "are plausibly indicated.\n\n"
    "For each pest you identify, decide a status:\n"
    "- \"confirmed\": the evidence is strong enough to move "
    "straight to advising the homeowner and recommending "
    "remediation, without asking for more evidence first. "
    "Photographic evidence that visually corroborates the report "
    "(e.g. a photo showing the same signs the homeowner "
    "described) is normally enough to justify \"confirmed\", even "
    "if the wording doesn't match any fixed keyword list.\n"
    "- \"suspected\": the report is plausible but not yet strong "
    "enough to act on -- more information (often a photo) would "
    "help confirm it.\n\n"
    "Strict rules:\n"
    "- Only report a pest when there is real supporting evidence "
    "in the report or photo description. Do not guess.\n"
    "- A hypothesis's confidence must be a number from 0.0 to 1.0.\n"
    "- Respond with ONLY a JSON object, no other text, matching "
    "this shape exactly:\n"
    '{"hypotheses": [{"name": "<pest activity name, e.g. '
    '\'Possible Cockroach Activity\' or \'Confirmed Rodent '
    'Infestation\'>", "confidence": <0.0-1.0>, "status": '
    '"suspected" | "confirmed", "description": "<one sentence>", '
    '"supporting_facts": ["<short fact>", ...]}]}\n'
    "- If nothing is clearly indicated, respond with exactly: "
    '{"hypotheses": []}'
)


class LLMUnderstandingStrategy(UnderstandingStrategy):
    """
    Turns a reported observation (and any photographic evidence)
    into hypotheses about which pest(s) are indicated, using an LLM
    instead of a fixed per-pest keyword rule catalog. This is what
    lets HIOS support new pest types without writing new rule files
    for each one, and lets a photo that corroborates an
    already-suspected pest raise it straight to "confirmed"
    (see HypothesisStatus) rather than always asking for another
    photo -- something a pure keyword match can't reliably do,
    since vision-model descriptions rarely repeat the exact
    keywords a hand-written rule was looking for.
    """

    def __init__(self, *, llm: AssistantLLM) -> None:
        self._llm = llm

    async def understand(
        self,
        request: UnderstandingRequest,
    ) -> UnderstandingResult:

        user_prompt = self._build_user_prompt(request)

        try:
            response = await self._llm.generate(
                system_prompt=_SYSTEM_PROMPT,
                user_prompt=user_prompt,
            )
        except Exception:
            return self._unclear_result()

        hypotheses = self._parse(response)

        if not hypotheses:
            return self._unclear_result()

        return UnderstandingResult(
            hypotheses=hypotheses,
            unknowns=[],
        )

    def _build_user_prompt(self, request: UnderstandingRequest) -> str:
        lines = [
            f"Homeowner's report: {request.observation or '(no text report)'}",
        ]

        if request.evidence:
            lines.append("")
            lines.append("Photographic evidence findings:")
            for item in request.evidence:
                lines.append(f"- {item}")

        if request.knowledge is not None and request.knowledge.facts:
            lines.append("")
            lines.append(
                "Additional signals from deterministic keyword "
                "rules (may be incomplete -- use your own "
                "judgement too):"
            )
            for fact in request.knowledge.facts:
                lines.append(f"- {fact}")

        return "\n".join(lines)

    def _parse(self, response: str) -> list[Hypothesis]:
        try:
            data = json.loads(response.strip())
        except (json.JSONDecodeError, TypeError, AttributeError):
            return []

        if not isinstance(data, dict):
            return []

        raw_hypotheses = data.get("hypotheses")

        if not isinstance(raw_hypotheses, list):
            return []

        hypotheses = []
        seen_ids: set[str] = set()

        for raw in raw_hypotheses:
            hypothesis = self._parse_one(raw, seen_ids)

            if hypothesis is not None:
                hypotheses.append(hypothesis)

        return hypotheses

    def _parse_one(self, raw, seen_ids: set[str]) -> Hypothesis | None:
        if not isinstance(raw, dict):
            return None

        name = raw.get("name")

        if not isinstance(name, str) or not name.strip():
            return None

        name = name.strip()

        confidence = raw.get("confidence", 0.5)

        try:
            confidence = float(confidence)
        except (TypeError, ValueError):
            confidence = 0.5

        confidence = max(0.0, min(1.0, confidence))

        status_raw = raw.get("status", "suspected")

        try:
            status = HypothesisStatus(str(status_raw).strip().lower())
        except ValueError:
            status = HypothesisStatus.SUSPECTED

        description = raw.get("description")

        if not isinstance(description, str) or not description.strip():
            description = name

        supporting_facts = raw.get("supporting_facts")

        if not isinstance(supporting_facts, list):
            supporting_facts = []

        supporting_facts = [
            str(fact)
            for fact in supporting_facts
            if isinstance(fact, (str, int, float))
        ]

        hypothesis_id = self._slugify(name)

        suffix = 2
        base_id = hypothesis_id

        while hypothesis_id in seen_ids:
            hypothesis_id = f"{base_id}-{suffix}"
            suffix += 1

        seen_ids.add(hypothesis_id)

        return Hypothesis(
            id=hypothesis_id,
            name=name,
            description=description.strip(),
            confidence=confidence,
            supporting_facts=supporting_facts,
            evidence=[],
            status=status,
        )

    @staticmethod
    def _slugify(name: str) -> str:
        slug = "".join(
            char.lower() if char.isalnum() else "-" for char in name
        )

        while "--" in slug:
            slug = slug.replace("--", "-")

        return slug.strip("-") or "pest"

    @staticmethod
    def _unclear_result() -> UnderstandingResult:
        return UnderstandingResult(
            hypotheses=[],
            unknowns=[
                Unknown(
                    description=(
                        "The nature and source of the reported "
                        "issue are not yet clear."
                    )
                )
            ],
        )