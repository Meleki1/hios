from typing import TypedDict
from hios.capabilities.assistant.models.assistant_domain import AssistantDomain
from hios.capabilities.assistant.models.home_context import HomeContext
from hios.capabilities.assistant.models.assistant_response import HomeAssistantResponse
from hios.capabilities.assistant.models.interaction_understanding import InteractionUnderstanding
from hios.capabilities.maintenance.models.maintenance_recommendation import MaintenanceRecommendation
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis
from hios.capabilities.assistant.models.outreach_decision import OutreachDecision
from hios.capabilities.outreach.contracts import OutreachResult



class HomeAssistantState(TypedDict, total=False):

    subject_id: str
    home_id: str
    conversation_id: str | None
    message: str
    image: bytes | None
    image_diagnosis: ImageDiagnosis | None

    understanding: InteractionUnderstanding | None
    knowledge: object | None
    memories: list[object]

    timeline: list[object]

    signals: list[object]
    risk: object | None
    prediction: object | None
    intent_score: object | None

    maintenance_recommendations: list[MaintenanceRecommendation]
    maintenance_records: list[object]

    outreach_decision: OutreachDecision | None
    outreach_result: OutreachResult | None
    outreach_recipient: str | None

    decision: object | None
    plan: object | None
    execution: object | None

    outcome: object | None

    reflection: object | None
    learning: object | None

    response: HomeAssistantResponse | None
    context: HomeContext | None
    domain: AssistantDomain | None
    metadata: dict