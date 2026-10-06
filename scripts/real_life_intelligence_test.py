"""
Real-life end-to-end test of the HIOS intelligence pipeline.

WHAT THIS DOES
---------------
Exercises the actual production code path -- HomeAssistantChat.send()
via hios.api.dependencies's real factories, the same ones FastAPI
uses -- with a real OpenAI account and a real local Postgres. Not
mocks, not fakes: a real multi-turn pest-control conversation, run
through the real LangGraph, the real AssistantResponseGenerationService
(real OpenAI calls), the real signal collectors, the real
RuleBasedIntentScorer, the real RuleBasedRiskEngine, and the real
BasicPredictionEngine -- then prints exactly what each of those
computed, plus what actually got persisted to Postgres (predictions,
timeline entries).

This also demonstrates the fix for a gap found during the September
2026 audit: HomeContextAssembler.assemble()'s `property_profile` is
None for every home in production today, because nothing ever
resolves a real address to a UPRN and links it (see
get_address_resolution_service()'s docstring in dependencies.py for
the full story). Without a property_profile, three of the five
signal categories (property/environmental/local_activity) never
fire. This script works around that gap for itself -- resolving a
real UK address and associating it with the demo home before
chatting -- specifically so the printed signals below are not
artificially empty. Production does not do this yet.

REQUIREMENTS
------------
- Local Postgres running and migrated:
    docker compose up -d postgres
    alembic upgrade head
    python -m hios.runtime.persistence.setup_checkpointer
- A real .env (copy .env.example -> .env and fill in):
    DATABASE_URL, OPENAI_API_KEY, HOMEDATA_API_KEY,
    TELEGRAM_BOT_TOKEN/TELEGRAM_WEBHOOK_SECRET/HIOS_BOOTSTRAP_SECRET
    are still required by Settings even though this script doesn't
    use Telegram -- see .env.example.

USAGE
-----
    python scripts/real_life_intelligence_test.py
    python scripts/real_life_intelligence_test.py --address "10 Downing Street, London" --postcode "SW1A 2AA"

This makes real OpenAI API calls (billed to your account) and a real
Homedata API call, and writes real rows to your local Postgres. Safe
to run repeatedly -- it reuses the same demo subject/home
(DEMO_SUBJECT_ID / DEMO_HOME_ID below) rather than creating a new one
every run, so conversation/timeline history accumulates across runs
the same way a real user's would.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import textwrap
import uuid

# Fixed, well-known demo identities so repeated runs accumulate
# history (return_visits, explicit_intent_history) the same way a
# real returning user's would, instead of starting fresh every time.
# Home has no subject_id field of its own (see Home/HomeService --
# the two are only ever associated implicitly, via whatever
# subject_id the caller passes alongside a home_id), and
# HomeRepository has no "get by subject_id" lookup, so this script
# pins both ids itself rather than going through
# HomeService.create() (which always mints a random home id) --
# that's the only way to make "run again and reuse the same demo
# home" possible without a new lookup method this script has no
# business adding to the real HomeService just for its own
# convenience.
DEMO_SUBJECT_ID = "00000000-0000-0000-0000-00000000d3d0"
DEMO_HOME_ID = "00000000-0000-0000-0000-00000000d3d1"
DEMO_HOME_NAME = "Real-Life Intelligence Test Home"

DEMO_CONVERSATION = [
    "Hi, I've started seeing droppings in my kitchen, near the "
    "pantry.",
    "It's been going on for about two weeks now and seems to be "
    "getting worse.",
    "How much would it cost to get someone out to treat it?",
    "Yes, please -- I'd like to go ahead and book a treatment.",
]


def _print_header(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def _print_model(label: str, model) -> None:
    print(f"\n--- {label} ---")
    if model is None:
        print("  None")
        return
    if isinstance(model, list):
        if not model:
            print("  [] (empty)")
        for item in model:
            _print_model("", item)
        return
    if hasattr(model, "model_dump"):
        for key, value in model.model_dump(mode="json").items():
            print(f"  {key}: {value}")
    else:
        print(f"  {model!r}")


async def main(address: str, postcode: str | None) -> None:
    # Imported inside main() rather than at module level so
    # `python scripts/real_life_intelligence_test.py --help` works
    # even without a configured .env (hios.db.session reads Settings
    # at import time -- see that module's docstring-equivalent
    # comment).
    from hios.core.config import get_settings
    from hios.db.session import SessionLocal
    from hios.runtime.persistence.checkpointer import (
        create_checkpointer,
    )
    from hios.api.dependencies import (
        get_address_resolution_service,
        get_home_assistant_graph,
        get_home_information_repository,
        get_home_property_service,
        get_home_repository,
        get_home_state_repository,
        get_timeline_service,
    )
    from hios.capabilities.assistant.chat import (
        ChatRequest,
        HomeAssistantChat,
    )
    from hios.capabilities.home.models.home import Home
    from hios.capabilities.home.models.home_information import (
        HomeInformation,
    )
    from hios.capabilities.home.models.home_state import HomeState

    get_settings()  # fail fast on missing config, same as main.py

    _print_header("1. Setting up demo home (real DB writes)")

    async with SessionLocal() as session:
        home_repository = get_home_repository(session)
        information_repository = get_home_information_repository(
            session,
        )
        state_repository = get_home_state_repository(session)
        home_property_service = get_home_property_service(session)

        home = await home_repository.get(DEMO_HOME_ID)

        if home is None:
            # Mirrors HomeService.create()'s own logic (see
            # hios/capabilities/home/services/home_service.py) but
            # with a pinned id, since that service always mints a
            # random one and has no parameter to override it.
            home = await home_repository.save(
                Home(
                    id=DEMO_HOME_ID,
                    name=DEMO_HOME_NAME,
                    home_type="residential",
                    description=(
                        "Created by "
                        "scripts/real_life_intelligence_test.py"
                    ),
                    status="active",
                )
            )
            await information_repository.save(
                HomeInformation(
                    home_id=home.id,
                    country="United Kingdom",
                    city="London",
                    address=address,
                    postcode=postcode,
                )
            )
            await state_repository.save(
                HomeState(
                    home_id=home.id,
                    status="active",
                )
            )
            print(f"Created new demo home: {home.id}")
        else:
            print(f"Reusing existing demo home: {home.id}")

        home_id = home.id

        existing_reference = await home_property_service.get_by_home(
            home_id,
        )

        if existing_reference is None:
            print(
                f"Resolving address via Homedata: {address!r}"
            )
            address_resolution_service = (
                get_address_resolution_service()
            )
            candidates = await address_resolution_service.search(
                address,
            )

            if len(candidates) == 1:
                await home_property_service.associate(
                    home_id=home_id,
                    uprn=candidates[0].uprn,
                )
                print(
                    f"Linked home to UPRN {candidates[0].uprn} "
                    f"({candidates[0].address})"
                )
            else:
                print(
                    f"Address resolved to {len(candidates)} "
                    "candidates (need exactly 1) -- property_profile "
                    "will be None for this run, same as it is for "
                    "every real home today. Try a more specific "
                    "--address/--postcode."
                )
        else:
            print(
                f"Home already linked to UPRN {existing_reference.uprn}"
            )

    _print_header(
        "2. Running a real multi-turn conversation "
        "(real OpenAI calls)"
    )

    conversation_id = f"real-life-test-{uuid.uuid4()}"

    async with (
        SessionLocal() as session,
        create_checkpointer() as checkpointer,
    ):
        # Idempotent -- CREATE TABLE IF NOT EXISTS under the hood.
        # See hios/runtime/persistence/setup_checkpointer.py, which
        # this mirrors so the script works even if that was never
        # run manually first.
        await checkpointer.setup()

        graph = get_home_assistant_graph(session, checkpointer)
        chat = HomeAssistantChat(graph=graph)

        for turn_number, message in enumerate(
            DEMO_CONVERSATION,
            start=1,
        ):
            print(f"\n[turn {turn_number}] You: {message}")

            response = await chat.send(
                ChatRequest(
                    subject_id=DEMO_SUBJECT_ID,
                    home_id=home_id,
                    message=message,
                    conversation_id=conversation_id,
                )
            )

            wrapped = textwrap.fill(
                response.message,
                width=74,
                initial_indent="  HIOS: ",
                subsequent_indent="        ",
            )
            print(wrapped)

        _print_header(
            "3. What the intelligence pipeline actually computed "
            "(final graph state)"
        )

        state_snapshot = await graph.aget_state(
            {
                "configurable": {
                    "thread_id": conversation_id,
                },
            },
        )
        values = state_snapshot.values

        _print_model("Signals collected", values.get("signals"))
        _print_model("Risk assessment", values.get("risk"))
        _print_model("Intent score", values.get("intent_score"))
        _print_model("Prediction", values.get("prediction"))
        _print_model(
            "Maintenance recommendations",
            values.get("maintenance_recommendations"),
        )
        _print_model(
            "Outreach decision",
            values.get("outreach_decision"),
        )
        _print_model(
            "Outreach result",
            values.get("outreach_result"),
        )

        _print_header(
            "4. What actually got persisted to Postgres (timeline)"
        )

        timeline_service = get_timeline_service(session)
        timeline = await timeline_service.get_by_subject(
            DEMO_SUBJECT_ID,
        )

        if not timeline:
            print("  (no timeline entries -- unexpected)")
        else:
            for entry in sorted(
                timeline,
                key=lambda e: e.created_at,
            ):
                print(
                    f"  [{entry.created_at.isoformat()}] "
                    f"{entry.event_type}.{entry.event_name} "
                    f"resource_id={entry.resource_id}"
                )

    _print_header("Done")
    print(
        "Run again to see return_visits / explicit_intent_history "
        "accumulate across runs for this same demo subject."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--address",
        default="10 Downing Street, London",
        help=(
            "A real UK address to resolve via Homedata and link to "
            "the demo home, so property/environmental/local_activity "
            "signals have something real to work with."
        ),
    )
    parser.add_argument(
        "--postcode",
        default="SW1A 2AA",
        help="Postcode for the demo home's stored HomeInformation.",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.address, args.postcode))
    except KeyboardInterrupt:
        sys.exit(1)