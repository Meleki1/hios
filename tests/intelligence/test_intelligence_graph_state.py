from hios.capabilities.intelligence.graph.state import (
    IntelligenceState,
)


def test_intelligence_state_can_hold_prediction_context():

    state: IntelligenceState = {
        "subject_id": "household-1",
        "target": "pest_control_need",
        "horizon_days": 14,
        "explicit_intents": [
            "reported_active_problem",
        ],
        "interactions": [
            "asked_about_pests",
        ],
        "local_activities": {
            "local_pest_reports": "increasing",
        },
        "platform_behaviours": {
            "return_visits": "3",
        },
    }

    assert state["subject_id"] == "household-1"
    assert state["target"] == "pest_control_need"
    assert state["horizon_days"] == 14

    assert (
        state["explicit_intents"]
        == ["reported_active_problem"]
    )

    assert (
        state["interactions"]
        == ["asked_about_pests"]
    )