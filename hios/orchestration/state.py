from typing import Any, TypedDict


class HIOSState(TypedDict, total=False):

    subject_id: str

    input: str

    signals: list[Any]

    intent_score: Any

    memories: list[Any]

    prediction: Any

    decision: Any

    execution: Any

    outcome: Any

    evaluation: Any

    errors: list[str]