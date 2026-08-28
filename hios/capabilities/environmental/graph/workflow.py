from langgraph.graph import END, START, StateGraph

from hios.capabilities.environmental.graph.nodes import (
    collect_environmental_data,
    produce_environmental_signals,
)
from hios.capabilities.environmental.graph.state import (
    EnvironmentalState,
)


def build_environmental_graph(
    environmental_service,
    collector,
):

    async def collect_node(
        state: EnvironmentalState,
    ):
        return await collect_environmental_data(
            state,
            environmental_service,
        )

    async def signal_node(
        state: EnvironmentalState,
    ):
        return await produce_environmental_signals(
            state,
            collector,
        )

    graph = StateGraph(
        EnvironmentalState,
    )

    graph.add_node(
        "collect_environmental_data",
        collect_node,
    )

    graph.add_node(
        "produce_environmental_signals",
        signal_node,
    )

    graph.add_edge(
        START,
        "collect_environmental_data",
    )

    graph.add_edge(
        "collect_environmental_data",
        "produce_environmental_signals",
    )

    graph.add_edge(
        "produce_environmental_signals",
        END,
    )

    return graph.compile()