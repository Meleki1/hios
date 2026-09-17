from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)


class ConversationSignalCollector:
    """
    "Progressive conversation signals" (product docs, category 2):
    the journey across a conversation -- not just its first message
    -- predicts intent ("Day 1: 'What's this insect?' ... Day 8:
    [books treatment]", more_info_HOME_AI.pdf).

    `interactions` is meant to be the caller's running history of
    explicit intents seen across the whole conversation so far (see
    `explicit_intent_history` in HomeAssistantState / the
    `intelligence` node in assistant/graph/nodes.py), not just this
    turn's -- a single message only ever produces 0-1 intents, so
    "progression" can only be observed by accumulating across turns.

    This used to check for a literal third vocabulary
    ("asked_about_pests", "asked_how_to_remove_them",
    "asked_about_treatment_price") that no collector anywhere ever
    produced -- not the explicit-intent vocabulary
    (AssistantInteractionUnderstandingService.ALLOWED_INTENTS /
    RuleBasedIntentScorer.WEIGHTS) and not anything else in the
    codebase, so this branch was unreachable in principle (flagged
    in the intelligence-pipeline-wiring-audit project doc, gap 5).
    Fixed to check for the real vocabulary: a user who has reported
    an active problem, asked what it costs, and asked for it to be
    treated has moved through the same funnel the docs describe,
    just expressed in the vocabulary this platform actually
    collects.
    """

    async def collect(
        self,
        subject_id: str,
        interactions: list[str],
    ) -> list[Signal]:

        signals = [
            Signal(
                type=SignalType.CONVERSATION,
                source=SignalSource.HOME_ASSIST,
                name="interaction",
                value=interaction,
            )
            for interaction in interactions
        ]

        progression = (
            "reported_active_problem" in interactions
            and "asked_for_price" in interactions
            and "requested_treatment" in interactions
        )

        if progression:
            signals.append(
                Signal(
                    type=SignalType.CONVERSATION,
                    source=SignalSource.HOME_ASSIST,
                    name="conversation_progression",
                    value="progressing_toward_treatment",
                )
            )

        return signals