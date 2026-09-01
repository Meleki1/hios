from typing import TypedDict, Annotated
from hios.capabilities.assistant.models.assistant_domain import AssistantDomain
from hios.capabilities.assistant.models.home_context import HomeContext
from hios.capabilities.assistant.models.assistant_response import HomeAssistantResponse
from hios.capabilities.assistant.models.interaction_understanding import InteractionUnderstanding
from hios.capabilities.maintenance.models.maintenance_recommendation import MaintenanceRecommendation
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis
from hios.capabilities.assistant.models.outreach_decision import OutreachDecision
from hios.capabilities.outreach.contracts import OutreachResult
from hios.capabilities.assistant.models.interaction_routing import InteractionRoutingResult
from hios.capabilities.execution.capability import ExecutionResult
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class HomeAssistantState(TypedDict, total=False):

    subject_id: str
    home_id: str
    conversation_id: str | None
    message: str
    image: bytes | None
    image_diagnosis: ImageDiagnosis | None

    messages: Annotated[list[BaseMessage], add_messages]

    understanding: InteractionUnderstanding | None
    knowledge: object | None
    memories: list[object]

    timeline: list[object]

    signals: list[object]
    risk: object | None
    prediction: object | None
    intent_score: object | None
    communicated_safety_guidance: list[str]
    maintenance_recommendations: list[MaintenanceRecommendation]
    maintenance_records: list[object]

    outreach_decision: OutreachDecision | None
    outreach_result: OutreachResult | None
    outreach_recipient: str | None

    decision: object | None
    plan: object | None
    execution: ExecutionResult | None

    outcome: object | None

    reflection: object | None
    learning: object | None

    response: HomeAssistantResponse | None
    domain: AssistantDomain | None
    routing: InteractionRoutingResult | None
    metadata: dict