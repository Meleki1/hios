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

Be concise, helpful, and conversational.
"""

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
{state.get("safety_guidance")}

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