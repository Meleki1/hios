from langgraph.graph import END, START, StateGraph

from hios.capabilities.property.graph.nodes import (
    enrich_property,
    resolve_property,
)
from hios.capabilities.property.graph.state import (
    PropertyState,
)


def build_property_graph(
    address_service,
    property_service,
):

    async def resolve_node(
        state: PropertyState,
    ):
        return await resolve_property(
            state,
            address_service,
        )

    async def enrich_node(
        state: PropertyState,
    ):
        return await enrich_property(
            state,
            property_service,
        )

    graph = StateGraph(PropertyState)

    graph.add_node(
        "resolve_property",
        resolve_node,
    )

    graph.add_node(
        "enrich_property",
        enrich_node,
    )

    graph.add_edge(
        START,
        "resolve_property",
    )

    graph.add_edge(
        "resolve_property",
        "enrich_property",
    )

    graph.add_edge(
        "enrich_property",
        END,
    )

    return graph.compile()