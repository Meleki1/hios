from hios.orchestration.state import HIOSState


def test_hios_state_can_hold_input():

    state: HIOSState = {
        "subject_id": "household-1",
        "input": "There are ants in my kitchen.",
    }

    assert state["subject_id"] == "household-1"
    assert state["input"] == (
        "There are ants in my kitchen."
    )