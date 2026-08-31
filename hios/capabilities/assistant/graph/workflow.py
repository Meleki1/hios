from langgraph.graph import END, START, StateGraph

from hios.capabilities.assistant.graph.state import (
    HomeAssistantState,
)
from hios.capabilities.assistant.context.home_context_assembler import (
    HomeContextAssembler,
)
from hios.capabilities.assistant.router.interaction_router import (
    InteractionRouter,
)

from hios.capabilities.assistant.graph.nodes import (
    create_nodes,
)
from hios.capabilities.assistant.response.assistant_action_response_builder import (
    AssistantActionResponseBuilder,
)
from hios.capabilities.assistant.services.response_generation import AssistantResponseGenerationService
from hios.capabilities.assistant.services.interaction_understanding import AssistantInteractionUnderstandingService
from hios.capabilities.assistant.models.assistant_domain import AssistantDomain


def route_after_understanding(
    state: HomeAssistantState,
) -> str:

    if state.get("domain") == AssistantDomain.PEST_CONTROL:
        return "dispatch_domain"

    return "intelligence"


def build_home_assistant_graph(
    *,
    context_assembler: HomeContextAssembler,
    router: InteractionRouter,
    hios,
    intelligence_graph,
    response_generation_service,
    interaction_understanding_service: (
        AssistantInteractionUnderstandingService
    ),
    checkpointer,
    image_diagnosis_service=None,
    maintenance_intelligence=None,
    outreach=None,
    outreach_policy=None,
    event_publisher=None,
):

    nodes = create_nodes(
        context_assembler=context_assembler,
        router=router,
        hios=hios,
        intelligence_graph=intelligence_graph,
        response_generation_service=response_generation_service,
        interaction_understanding_service=(
            interaction_understanding_service
        ),
        image_diagnosis_service=image_diagnosis_service,
        maintenance_intelligence=maintenance_intelligence,
        outreach=outreach,
        outreach_policy=outreach_policy,
        event_publisher=event_publisher,
        action_response_builder=AssistantActionResponseBuilder()
    )

    graph = StateGraph(
        HomeAssistantState,
    )

    graph.add_node(
        "assemble_context",
        nodes["assemble_context"],
    )

    graph.add_node(
        "route_interaction",
        nodes["route_interaction"],
    )

    graph.add_node(
        "understand_interaction",
        nodes["understand_interaction"],
    )

    graph.add_node(
        "diagnose_image",
        nodes["diagnose_image"],
    )

    graph.add_node(
        "decide_outreach",
        nodes["decide_outreach"],
    )

    graph.add_node(
        "execute_outreach",
        nodes["execute_outreach"],
    )

    graph.add_node(
        "intelligence",
        nodes["intelligence"],
    )

    graph.add_node(
        "dispatch_domain",
        nodes["dispatch_domain"],
    )

    graph.add_node(
        "build_response",
        nodes["build_response"],
    )

    graph.add_edge(
        START,
        "assemble_context",
    )

    graph.add_edge(
        "assemble_context",
        "route_interaction",
    )

    graph.add_edge(
        "route_interaction",
        "diagnose_image",
    )

    graph.add_edge(
        "diagnose_image",
        "understand_interaction",
    )

    graph.add_conditional_edges(
        "understand_interaction",
        route_after_understanding,
        {
            "dispatch_domain": "dispatch_domain",
            "intelligence": "intelligence",
        },
    )

    graph.add_edge(
        "intelligence",
        "dispatch_domain",
    )

    graph.add_edge(
        "dispatch_domain",
        "decide_outreach",
    )

    graph.add_edge(
        "decide_outreach",
        "execute_outreach",
    )

    graph.add_edge(
        "execute_outreach",
        "build_response",
    )

    graph.add_edge(
        "build_response",
        END,
    )
    return graph.compile(
        checkpointer=checkpointer,
    )