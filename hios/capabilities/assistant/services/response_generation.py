from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.llm.contract import AssistantLLM


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
You are the conversational intelligence of HIOS,
a Home Intelligence Operating System.

Your job is to communicate the result of HIOS processing
clearly and naturally to the user.

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
            "Present — will be appended after your message. "
            "Do not describe or guess its contents."
            if safety_guidance is not None
            and safety_guidance.guidance
            else "None for this interaction."
        )

        user_prompt = f"""
User message:
{state["message"]}

Home context:
{state.get("context")}

Understanding:
{state.get("understanding")}

Reported observation:
{state.get("observation")}

Assessment:
{state.get("assessment")}

Safety guidance:
{safety_guidance_note}

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

Decision:
{state.get("decision")}

Plan:
{state.get("plan")}

Execution:
{state.get("execution")}

Outcome:
{state.get("outcome")}

Reflection:
{state.get("reflection")}

Learning:
{state.get("learning")}
"""

        return await self._llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )