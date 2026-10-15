import re
from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.llm.contract import AssistantLLM
from hios.capabilities.execution.models.action import ActionType


_LEAKED_SAFETY_SECTION = re.compile(
    r"(?:^|\n)\s*(?:safety guidance|safety tips|precautions)\s*:?\s*\n"
    r"(?:[ \t]*[-•*]?\s*.+(?:\n|$))+",
    re.IGNORECASE | re.MULTILINE,
)

_LEAKED_AUTOMATIC_FOLLOWUP_PATTERNS = (
    re.compile(
        r"\s*safety guidance will be appended after your message\.?\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*a standard photo request will be appended after your message\.?\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*do not ask for photos or write safety guidance yourself\.?\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*handled automatically, do not write anything about it yourself\.?\s*",
        re.IGNORECASE,
    ),
)

_LEAKED_PHOTO_REQUEST_PATTERNS = (
    re.compile(
        r"\s*please share (?:the )?image when you(?:'re| are) ready\.?\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*(?:could you (?:please )?)?(?:provide|send)(?: me)? "
        r"(?:an )?(?:image|photo|picture)[^.!?]*[.!?]\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*(?:I(?:'ll| will)|we(?:'ll| will)|I) need[^.!?]*"
        r"visual evidence[^.!?]*[.!?]\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*(?:I'd like|I would like)[^.!?]*"
        r"(?:photo|image|picture|visual evidence)[^.!?]*[.!?]\s*",
        re.IGNORECASE,
    ),
    re.compile(
        r"\s*(?:share|send)(?: me)? (?:an? )?(?:image|photo|picture)"
        r"[^.!?]*[.!?]\s*",
        re.IGNORECASE,
    ),
)

class AssistantResponseGenerationService:

    def __init__(
        self,
        *,
        llm: AssistantLLM,
    ) -> None:
        self._llm = llm

    async def generate(
        self,
        *,
        state: HomeAssistantState,
    ) -> str:
        system_prompt = """
You are HIOS — the Home Intelligence Operating System.
"HIOS" is both your name and how you refer to yourself; the
user does not need to call you anything else, and you should
sign off or refer to yourself as HIOS rather than "the
assistant," "the system," or similar.

Your job is to communicate the result of HIOS processing
clearly and naturally to the user.

Vision and current scope: HIOS is being built to help
homeowners with whatever comes up about their home — pest
issues, maintenance, and more over time. Right now, only
pest control is actually live; everything else is on the
roadmap, not yet available. Be upfront about this rather
than implying broader capability than you actually have.

When to introduce yourself: you are told below whether this
is the first message of the conversation. If it is, or the
user is explicitly asking who you are or what you can do
(at any point in the conversation), briefly introduce
yourself as HIOS (the Home Intelligence Operating System),
mention the broader vision in one sentence, and note that
today you can help specifically with pest control, with more
home capabilities coming soon. Keep it short — a couple of
sentences, not a pitch. If it is not the first message and
the user isn't asking who you are, don't re-introduce
yourself — just respond normally.

When the user's message is about a real home issue that is
not pest control (you will be told the routed domain below
— "home" means exactly this: a genuine home problem that
isn't pest-related), say plainly and warmly that you can't
help with that particular issue yet, that pest control is
the only thing HIOS handles right now, and that it's exactly
the kind of thing more home capabilities will cover as they
roll out. Don't apologize excessively or make it sound like
a failure — a young product still growing into its full
scope is normal and expected. Do not attempt to answer the
underlying home question yourself (no invented advice about
plumbing, electrical, roofing, etc.) even if you happen to
know something about it — that's out of scope for you today.

When the domain is "unsupported" (the request isn't about
the user's home at all), decline briefly and warmly, and
mention you're built to help with home-related things —
right now specifically pest control — rather than leaving
the decline unexplained.

Use only the information provided in the HIOS state.
Do not invent facts, actions, diagnoses, decisions, or
recommendations.

If information is uncertain, communicate that uncertainty.

Be concise, helpful, and conversational. Write in plain
prose only — no markdown. Do not use asterisks or
underscores for bold/italic, no "#" headers, and no
numbered or bulleted lists formatted with markdown syntax
(a plain "1. ..." sentence is fine; "**Step 1**: ..." is
not). This text is sent as-is to a chat client that does
not render markdown, so any markdown characters would show
up literally instead of as formatting.

Some replies have extra text appended after yours by the
platform (see append_flags below). You are not shown that
wording. Never mention append flags, appended blocks, or
anything that will follow your message. Do not use phrases
like "see below", "as noted above", or "will be included
after this message".

When precautions_block is yes: do not write precaution
lists, do not use headings such as Precautions or Safety
tips, and do not open with bulleted or numbered precaution
items — even from general knowledge. Start with plain prose
about what was reported and what it suggests.

When photo_request_block is yes: do not ask for a photo,
image, or visual evidence yourself. Describe the situation;
the platform adds the standard photo ask separately.
"""

        domain = state.get("domain")
        domain_note = (
            domain.value if domain is not None else "unknown"
        )

        is_first_turn = len(state.get("messages", [])) <= 1

        user_prompt = f"""
User message:
{state["message"]}

Is this the first message of the conversation?
{"Yes." if is_first_turn else "No."}

Routed domain (conversation | home | pest_control |
unsupported): {domain_note}

Home context:
{state.get("context")}

Understanding:
{state.get("understanding")}

Reported observation:
{state.get("observation")}

Assessment:
{state.get("assessment")}

Append flags (internal — never mention to the user):
{self._build_append_flags(state)}

Signals:
{state.get("signals", [])}

Risk:
{state.get("risk")}

Prediction:
{state.get("prediction")}

Intent score:
{state.get("intent_score")}

Maintenance recommendations:
{state.get("maintenance_recommendations", [])}

Outcome:
{state.get("outcome")}

Reflection:
{state.get("reflection")}

Learning:
{state.get("learning")}
"""

        message = await self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return self._sanitize_llm_message(message)

    def _build_append_flags(
        self,
        state: HomeAssistantState,
    ) -> str:

        safety_guidance = state.get("safety_guidance")
        precautions_block = (
            safety_guidance is not None
            and bool(safety_guidance.guidance)
        )
        photo_request_block = self._will_append_photo_request(
            state,
        )

        return (
            f"precautions_block: "
            f"{'yes' if precautions_block else 'no'}\n"
            f"photo_request_block: "
            f"{'yes' if photo_request_block else 'no'}"
        )

    def _will_append_photo_request(
        self,
        state: HomeAssistantState,
    ) -> bool:

        execution_result = state.get("execution")
        if execution_result is None:
            return False

        execution = getattr(
            execution_result,
            "execution",
            None,
        )
        if execution is None:
            actions = getattr(
                execution_result,
                "actions",
                None,
            )
        else:
            actions = getattr(
                execution,
                "actions",
                None,
            )

        if not actions:
            return False

        return any(
            action.action_type == ActionType.IMAGE_REQUEST
            for action in actions
        )

    def _sanitize_llm_message(
        self,
        message: str,
    ) -> str:

        if not message:
            return message

        message = self._strip_all_leaked_safety_sections(
            message,
        )
        message = self._strip_leaked_automatic_followup_notes(
            message,
        )
        message = self._strip_leaked_photo_requests(
            message,
        )

        message = re.sub(
            r"\n{3,}",
            "\n\n",
            message,
        )

        return message.strip()

    def _strip_all_leaked_safety_sections(
        self,
        message: str,
    ) -> str:

        previous = None
        while previous != message:
            previous = message
            message = _LEAKED_SAFETY_SECTION.sub(
                "",
                message,
            )

        return message.strip()

    def _strip_leaked_automatic_followup_notes(
        self,
        message: str,
    ) -> str:

        for pattern in _LEAKED_AUTOMATIC_FOLLOWUP_PATTERNS:
            message = pattern.sub(
                "",
                message,
            )

        return message.strip()

    def _strip_leaked_photo_requests(
        self,
        message: str,
    ) -> str:

        for pattern in _LEAKED_PHOTO_REQUEST_PATTERNS:
            message = pattern.sub(
                "",
                message,
            )

        return message.strip()