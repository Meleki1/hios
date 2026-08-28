from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)

from hios.capabilities.assistant.router.interaction_router import (
    InteractionRouter,
)


class DefaultInteractionRouter(
    InteractionRouter,
):

    def route(
        self,
        message: str,
    ) -> AssistantDomain:

        normalized = message.strip().lower()

        if not normalized:
            return AssistantDomain.CONVERSATION

        if normalized in {
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "thanks",
            "thank you",
            "bye",
            "goodbye",
        }:
            return AssistantDomain.CONVERSATION

        pest_terms = {
            "pest",
            "pests",
            "rat",
            "rats",
            "mouse",
            "mice",
            "ant",
            "ants",
            "cockroach",
            "cockroaches",
            "termite",
            "termites",
            "bed bug",
            "bed bugs",
            "insect",
            "insects",
        }

        if any(
            term in normalized
            for term in pest_terms
        ):
            return AssistantDomain.PEST_CONTROL

        home_terms = {
            "my home",
            "my house",
            "my property",
            "about my home",
            "about my house",
            "about my property",
        }

        if any(
            term in normalized
            for term in home_terms
        ):
            return AssistantDomain.HOME

        return AssistantDomain.UNSUPPORTED