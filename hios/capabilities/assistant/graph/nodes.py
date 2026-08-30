from __future__ import annotations
from hios.core.events.base_event import BaseEvent
from hios.capabilities.assistant.context.home_context_assembler import HomeContextAssembler
from hios.capabilities.assistant.graph.state import HomeAssistantState
from hios.capabilities.assistant.router.interaction_router import InteractionRouter
from hios.capabilities.assistant.models.assistant_domain import AssistantDomain
from hios.capabilities.pest_control.contract import PestControlRequest
from hios.capabilities.assistant.models.assistant_response import HomeAssistantResponse
from hios.capabilities.assistant.models.interaction_understanding import InteractionUnderstanding
from hios.capabilities.assistant.response.assistant_action_response_builder import AssistantActionResponseBuilder
from hios.capabilities.assistant.models.outreach_decision import OutreachDecision
from hios.capabilities.outreach.contracts import OutreachRequest, OutreachResult
from hios.capabilities.outreach.models import OutreachChannel, OutreachDeliveryStatus
from hios.runtime.context import RuntimeContext
from hios.capabilities.outreach.policy import DefaultOutreachPolicy
from hios.capabilities.assistant.services.response_generation import AssistantResponseGenerationService
from hios.capabilities.assistant.services.interaction_understanding import AssistantInteractionUnderstandingService



def create_nodes(
    *,
    context_assembler: HomeContextAssembler,
    router: InteractionRouter,
    hios,
    intelligence_graph,
    response_generation_service: AssistantResponseGenerationService,
    interaction_understanding_service: (
        AssistantInteractionUnderstandingService
    ),
    maintenance_intelligence=None,
    outreach=None,
    outreach_service=None,
    action_response_builder: AssistantActionResponseBuilder,
    image_diagnosis_service=None,
    outreach_policy=None,
    event_publisher=None,
):

    async def assemble_context(
        state: HomeAssistantState,
    ) -> dict:

        context = await context_assembler.assemble(
            home_id=state["home_id"],
            subject_id=state["subject_id"],
            message=state["message"],
        )

        return {
            "context": context,
        }

    async def route_interaction(
        state: HomeAssistantState,
    ) -> dict:

        domain = router.route(
            state["message"],
        )

        return {
            "domain": domain,
        }

    async def dispatch_domain(
        state: HomeAssistantState,
    ) -> dict:

        maintenance_recommendations = state.get(
            "maintenance_recommendations",
            [],
        )

        if maintenance_recommendations:
            return {}

        domain = state["domain"]

        if domain == AssistantDomain.PEST_CONTROL:
            result = await hios.execute(
                PestControlRequest(
                    subject_id=state["subject_id"],
                    home_id=state["home_id"],
                    message=state["message"],
                )
            )

            return {
                "decision": result.decision,
                "plan": result.plans,
                "execution": result.execution,
                "outcome": result.outcome,
                "reflection": result.reflection,
                "learning": result.learning,
            }

        return {}

    async def build_response(
        state: HomeAssistantState,
    ) -> dict:
        maintenance_recommendations = (
            state.get(
                "maintenance_recommendations",
                [],
            )
        )

        if maintenance_recommendations:
            recommendation = (
                maintenance_recommendations[0]
            )

            return {
                "response": HomeAssistantResponse(
                    message=(
                        f"I recommend scheduling "
                        f"{recommendation.task}. "
                        f"{recommendation.reason}"
                    ),
                    conversation_id=state.get(
                        "conversation_id",
                    ),
                    capability="maintenance",
                    metadata={
                        "task": recommendation.task,
                        "maintenance_type": (
                            recommendation.maintenance_type
                        ),
                        "priority": recommendation.priority,
                    },
                )
            }

        actions = []

        execution = state.get("execution")

        if execution is not None and execution.execution is not None:
            actions = execution.execution.actions

        action_response = action_response_builder.build(
            actions=actions,
            conversation_id=state.get(
                "conversation_id",
            ),
        )

        if action_response is not None:
            return {
                "response": action_response,
            }

        message = await response_generation_service.generate(
            state=state,
        )

        domain = state.get("domain")

        return {
            "response": HomeAssistantResponse(
                message=message,
                conversation_id=state.get(
                    "conversation_id",
                ),
                capability=(
                    domain.value
                    if domain is not None
                    else None
                ),
                metadata={},
            )
        }
    
    async def understand_interaction(
        state: HomeAssistantState,
    ) -> dict:
        understanding = (
            await interaction_understanding_service.understand(
                state=state,
            )
        )

        return {
            "understanding": understanding,
        }

    async def diagnose_image(
        state: HomeAssistantState,
    ) -> dict:

        image = state.get("image")

        if not image:
            return {}

        diagnosis = await image_diagnosis_service.diagnose(
            image=image,
        )

        return {
            "image_diagnosis": diagnosis,
        }

    async def intelligence(
        state: HomeAssistantState,
    ) -> dict:

        understanding = state.get(
            "understanding",
        )

        explicit_intents = []

        if understanding is not None:
            explicit_intents = (
                understanding.explicit_intents
            )

        context = state.get(
            "context",
        )

        timeline = []

        if context is not None:
            timeline = context.timeline

        intelligence_state = {
            "subject_id": state["subject_id"],
            "target": "home_maintenance",
            "horizon_days": 30,
            "explicit_intents": explicit_intents,
            "timeline": timeline,
        }

        result = await intelligence_graph.ainvoke(
            intelligence_state,
        )

        maintenance_records = []

        if context is not None:
            maintenance_records = context.maintenance_records

        maintenance_recommendations = []

        if maintenance_intelligence is not None:
            maintenance_recommendations = (
                await maintenance_intelligence.analyze(
                    subject_id=state["subject_id"],
                    home_id=state["home_id"],
                    timeline=timeline,
                    maintenance_records=maintenance_records,
                    explicit_intents=explicit_intents,
                )
            )

        return {
            "signals": result.get(
                "signals",
                [],
            ),
            "risk": result.get(
                "risk",
            ),
            "intent_score": result.get(
                "intent_score",
            ),
            "prediction": result.get(
                "prediction",
            ),
            "maintenance_recommendations": (
                maintenance_recommendations
            ),
        }

    async def decide_outreach(
        state: HomeAssistantState,
    ) -> dict:

        recommendations = state.get(
            "maintenance_recommendations",
            [],
        )
        outreach_policy = DefaultOutreachPolicy()

        if not recommendations:
            return {
                "outreach_decision": None,
            }

        if outreach_policy is None:
            return {
                "outreach_decision": None,
            }

        recommendation = recommendations[0]

        context = state.get("context")

        timeline = []

        if context is not None:
            timeline = context.timeline

        decision = outreach_policy.decide(
            recommendation,
            timeline,
        )

        return {
            "outreach_decision": decision,
        }

    async def execute_outreach(
            state: HomeAssistantState,
        ) -> dict:

            outreach_decision = state.get(
                "outreach_decision",
            )

            if outreach_decision is None:
                return {}

            if not outreach_decision.required:
                return {}

            if outreach is None:
                raise RuntimeError(
                    "Outreach capability is required "
                    "for an outreach decision."
                )

            recommendations = state.get(
                "maintenance_recommendations",
                [],
            )

            if not recommendations:
                return {}

            recommendation = recommendations[0]

            recipient = state.get(
                "metadata",
                {},
            ).get("email")

            if not recipient:
                raise ValueError(
                    "No email recipient available for outreach."
                )

            result = await outreach.reason(
                OutreachRequest(
                    recipient=recipient,
                    subject=(
                        f"HIOS Maintenance Alert: "
                        f"{recommendation.task}"
                    ),
                    message=(
                        f"HIOS Maintenance Alert\n\n"
                        f"Task: {recommendation.task}\n"
                        f"Reason: {recommendation.reason}\n"
                        f"Priority: {recommendation.priority}"
                    ),
                    channel=OutreachChannel.EMAIL,
                ),
                RuntimeContext(),
            )

            if (
                result.status == OutreachDeliveryStatus.SENT
                and event_publisher is not None
            ):
                await event_publisher.publish(
                    BaseEvent(
                        event_type="outreach",
                        event_name="maintenance_alert_sent",
                        state="sent",
                        description=(
                            f"Maintenance alert sent: "
                            f"{recommendation.task}"
                        ),
                        subject_id=state["subject_id"],
                        resource_id=recommendation.task,
                        resource_type="maintenance",
                    )
                )

            return {
                "outreach_result": result,
            }


    return {
        "assemble_context": assemble_context,
        "diagnose_image": diagnose_image,
        "route_interaction": route_interaction,
        "understand_interaction": understand_interaction,
        "intelligence": intelligence,
        "decide_outreach": decide_outreach,
        "execute_outreach": execute_outreach,
        "dispatch_domain": dispatch_domain,
        "build_response": build_response,
    }