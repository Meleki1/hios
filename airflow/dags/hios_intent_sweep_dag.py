from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime

from airflow.decorators import dag, task
from airflow.models import Variable

logger = logging.getLogger(__name__)


def _load_targets() -> list[dict]:
    raw = Variable.get(
        "HIOS_SWEEP_TARGETS",
        default_var="[]",
    )

    try:
        targets = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(
            "HIOS_SWEEP_TARGETS is not valid JSON (%r) -- "
            "treating as empty.",
            raw,
        )
        return []

    if not isinstance(targets, list):
        logger.warning(
            "HIOS_SWEEP_TARGETS must be a JSON array of "
            "{subject_id, home_id} objects -- got %r.",
            type(targets),
        )
        return []

    return targets


async def _sweep_one(session, subject_id: str, home_id: str) -> dict:
    # Imported lazily, inside the task, so DAG *parsing* (which
    # Airflow does frequently, on every scheduler loop) never needs
    # hios's settings/DB to be reachable -- only actually *running*
    # the task does. hios/db/session.py reads Settings at import
    # time, so importing this any earlier would make a misconfigured
    # .env break DAG parsing for every DAG, not just this one.
    from hios.api.dependencies import (
        get_environmental_service,
        get_home_context_assembler,
        get_intelligence_pipeline,
    )

    context_assembler = get_home_context_assembler(session)
    environmental_service = get_environmental_service()
    pipeline = get_intelligence_pipeline(session)

    context = await context_assembler.assemble(
        home_id=home_id,
        subject_id=subject_id,
        message="",
    )

    property_profile = context.property_profile

    environmental_observation = None

    if (
        property_profile is not None
        and property_profile.latitude is not None
        and property_profile.longitude is not None
    ):
        try:
            environmental_observation = (
                await environmental_service.get_observation(
                    latitude=property_profile.latitude,
                    longitude=property_profile.longitude,
                )
            )
        except Exception:
            logger.exception(
                "Environmental lookup failed for home %s; "
                "continuing without it.",
                home_id,
            )

    prediction = await pipeline.predict(
        subject_id=subject_id,
        target="home_maintenance",
        horizon_days=30,
        property_profile=property_profile,
        environmental_observation=environmental_observation,
    )

    return {
        "subject_id": subject_id,
        "home_id": home_id,
        "prediction_id": prediction.id,
        "intent_level": prediction.intent_score.level.value,
        "intent_score": prediction.intent_score.score,
        "probability": prediction.probability,
        "evidence": prediction.evidence,
    }


async def _run_sweep(targets: list[dict]) -> list[dict]:
    # Imported lazily -- see the comment in _sweep_one.
    from hios.db.session import SessionLocal

    results = []

    async with SessionLocal() as session:
        for target in targets:
            subject_id = target.get("subject_id")
            home_id = target.get("home_id")

            if not subject_id or not home_id:
                logger.warning(
                    "Skipping malformed sweep target: %r",
                    target,
                )
                continue

            try:
                result = await _sweep_one(
                    session,
                    subject_id,
                    home_id,
                )
                results.append(result)
                logger.info(
                    "Intent sweep for home %s: %s (score=%.1f, "
                    "probability=%s)",
                    home_id,
                    result["intent_level"],
                    result["intent_score"],
                    result["probability"],
                )
            except Exception:
                logger.exception(
                    "Intent sweep failed for subject=%s home=%s",
                    subject_id,
                    home_id,
                )

    return results


@dag(
    dag_id="hios_intent_sweep",
    description=(
        "Proactively re-scores intent/prediction for configured "
        "homes using the real HIOS intelligence pipeline."
    ),
    schedule="0 */6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["hios", "intelligence", "example"],
)
def hios_intent_sweep():

    @task
    def run_sweep():
        targets = _load_targets()

        if not targets:
            logger.info(
                "No HIOS_SWEEP_TARGETS configured (Airflow "
                "Variable) -- nothing to sweep. Set it to a JSON "
                'array like [{"subject_id": "...", "home_id": '
                '"..."}] to try this against a real home.'
            )
            return []

        return asyncio.run(_run_sweep(targets))

    run_sweep()


hios_intent_sweep()
