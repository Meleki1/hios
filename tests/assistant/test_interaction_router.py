from hios.capabilities.assistant.models.assistant_domain import (
    AssistantDomain,
)

from hios.capabilities.assistant.router.default_interaction_router import (
    DefaultInteractionRouter,
)


def test_router_recognizes_pleasantry():

    router = DefaultInteractionRouter()

    assert (
        router.route("Hello")
        == AssistantDomain.CONVERSATION
    )


def test_router_recognizes_home_query():

    router = DefaultInteractionRouter()

    assert (
        router.route(
            "Tell me about my home"
        )
        == AssistantDomain.HOME
    )


def test_router_recognizes_pest_control_request():

    router = DefaultInteractionRouter()

    assert (
        router.route(
            "I found rats in my kitchen"
        )
        == AssistantDomain.PEST_CONTROL
    )


def test_router_rejects_unsupported_domain():

    router = DefaultInteractionRouter()

    assert (
        router.route(
            "My boiler isn't working"
        )
        == AssistantDomain.UNSUPPORTED
    )


def test_router_handles_empty_message():

    router = DefaultInteractionRouter()

    assert (
        router.route("")
        == AssistantDomain.CONVERSATION
    )