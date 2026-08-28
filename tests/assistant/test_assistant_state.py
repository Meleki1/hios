from hios.capabilities.assistant.graph.state import (
    HomeAssistantState,
)


def test_home_assistant_state_contains_request_context():

    state: HomeAssistantState = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "conversation_id": "conversation-123",
        "message": "I noticed scratching in the loft.",
    }

    assert state["subject_id"] == "subject-123"
    assert state["home_id"] == "home-123"
    assert state["conversation_id"] == (
        "conversation-123"
    )
    assert state["message"] == (
        "I noticed scratching in the loft."
    )

def test_home_assistant_state_can_hold_capability_results():

    state: HomeAssistantState = {
        "subject_id": "subject-123",
        "home_id": "home-123",
        "message": "I noticed scratching in the loft.",
        "signals": [],
        "memories": [],
        "timeline": [],
        "risk": None,
        "prediction": None,
        "decision": None,
        "plan": None,
        "execution": None,
        "outcome": None,
        "reflection": None,
        "learning": None,
        "response": "I can help with that.",
    }

    assert state["signals"] == []
    assert state["memories"] == []
    assert state["timeline"] == []
    assert state["response"] == (
        "I can help with that."
    )