from langgraph.graph import END, START, StateGraph

from hios.capabilities.intelligence.graph.nodes import collect_and_score, predict, assess_risk
from hios.capabilities.intelligence.graph.state import (
    IntelligenceState,
)


def build_intelligence_graph(
    signal_collection_service,
    intelligence_service,
    risk_assessment_service,
    risk_signal_adapter,
):

    async def assess_risk_node(
        state: IntelligenceState,
    ):
        return await assess_risk(
            state=state,
            risk_assessment_service=(
                risk_assessment_service
            ),
            risk_signal_adapter=(
                risk_signal_adapter
            ),
        )

    async def collect_and_score_node(
        state: IntelligenceState,
    ):
        return await collect_and_score(
            state=state,
            signal_collection_service=(
                signal_collection_service
            ),
        )

    async def predict_node(
        state: IntelligenceState,
    ):
        return await predict(
            state=state,
            intelligence_service=intelligence_service,
        )

    graph = StateGraph(
        IntelligenceState,
    )

    graph.add_node(
        "assess_risk",
        assess_risk_node,
    )

    graph.add_node(
        "collect_and_score",
        collect_and_score_node,
    )

    graph.add_node(
        "predict",
        predict_node,
    )

    graph.add_edge(
        START,
        "assess_risk",
    )

    graph.add_edge(
        "assess_risk",
        "collect_and_score",
    )

    graph.add_edge(
        "collect_and_score",
        "predict",
    )

    graph.add_edge(
        "predict",
        END,
    )

    return graph.compile()