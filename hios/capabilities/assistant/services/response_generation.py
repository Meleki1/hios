import re
from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.llm.contract import AssistantLLM
from hios.capabilities.execution.models.action import ActionType


_LEAKED_SAFETY_SECTION = re.compile(
    r"(?:^|\n)\s*(?:safety guidance|safety tips|precautions)\s*:?\s*\n"
    r"(?:[ \t]*[-•*]?\s*.+(?:\n|$))+",
    re.IGNORECASE | re.MULTILINE,
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

You are not told the exact wording of the safety guidance
for this interaction — only whether any exists. That is
deliberate: if present, it is appended to your message
automatically, verbatim, as its own clearly-separated list
right after your message, so you cannot repeat content you
were never shown. Do not mention it, guess its contents, or
refer to where it appears ("see below," "as noted above,"
etc.) — it needs no introduction, it will simply follow your
message as its own section. Just write your part of the
message as if the guidance weren't there at all.

This means: never write a heading or label such as "Safety
guidance", "Safety tips", "Precautions", or similar, and
never open your reply with a bulleted or numbered list of
your own safety recommendations — even generic ones drawn
from your own knowledge of the topic. That entire concern
belongs exclusively to the automatically-appended section,
not to you. Your reply should always begin with the
narrative — what was reported and what it suggests — never
with anything resembling a safety section.

Similarly, do not ask the user to send a photo yourself,
and do not ask whether they can provide one. When a photo is
actually needed, a separate, standard request for one is
appended automatically after your message — asking for it
yourself would duplicate that request. Just describe what
was reported and what it suggests; let the automatic request
(if any) be the only place a photo is asked for.
"""

        safety_guidance = state.get("safety_guidance")
        safety_guidance_note = (
            "Yes — handled automatically, do not write "
            "anything about it yourself."
            if safety_guidance is not None
            and safety_guidance.guidance
            else "No."
        )

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

Is separate safety guidance being sent automatically after
your message? {safety_guidance_note}

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

Automatic follow-ups appended after your message (do not duplicate):
{self._build_automatic_followups_note(state)}

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

    def _build_automatic_followups_note(
        self,
        state: HomeAssistantState,
    ) -> str:

        lines: list[str] = []

        safety_guidance = state.get("safety_guidance")
        if (
            safety_guidance is not None
            and safety_guidance.guidance
        ):
            lines.append(
                "- Safety guidance will be appended after your message."
            )

        if self._will_append_photo_request(state):
            lines.append(
                "- A standard photo request will be appended "
                "after your message."
            )

        if not lines:
            return "None."

        return (
            "\n".join(lines)
            + "\n(Do not ask for photos or write safety guidance yourself.)"
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