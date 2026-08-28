from hios.capabilities.intelligence.graph.state import IntelligenceState
from hios.capabilities.intelligence.signal_collection_service import SignalCollectionService
from hios.capabilities.intelligence.intelligence_service import IntelligenceService
from hios.capabilities.risk.risk_assessment_service import RiskAssessmentService
from hios.capabilities.risk.risk_signal_adapter import RiskSignalAdapter


async def collect_and_score(
    state: IntelligenceState,
    signal_collection_service: SignalCollectionService,
) -> dict:

    signals = await signal_collection_service.collect(
        subject_id=state["subject_id"],
        property_profile=state.get(
            "property_profile",
        ),
        environmental_observation=state.get(
            "environmental_observation",
        ),
        explicit_intents=state.get(
            "explicit_intents",
        ),
        interactions=state.get(
            "interactions",
        ),
        local_activities=None,
        platform_behaviours=state.get(
            "platform_behaviours",
        ),
    )

    # Include risk signals produced by the
    # previous risk-assessment stage.
    risk_signals = state.get(
        "risk_signals",
        [],
    )

    signals.extend(
        risk_signals,
    )

    local_activity_provider_results = []

    property_profile = state.get(
        "property_profile",
    )

    if (
        property_profile is not None
        and property_profile.latitude is not None
        and property_profile.longitude is not None
    ):

        (
            local_activity_signals,
            local_activity_provider_results,
        ) = (
            await signal_collection_service
            .collect_local_activity_with_status(
                subject_id=state["subject_id"],
                property_profile=property_profile,
                radius_km=5.0,
            )
        )

        signals.extend(
            local_activity_signals,
        )

    intent_score = (
        await signal_collection_service.score_signals(
            signals,
        )
    )

    return {
        "intent_score": intent_score,
        "local_activity_provider_results": (
            local_activity_provider_results
        ),
    }

async def predict(
    state: IntelligenceState,
    intelligence_service: IntelligenceService,
) -> dict:

    prediction = await intelligence_service.predict(
        subject_id=state["subject_id"],
        target=state["target"],
        horizon_days=state["horizon_days"],
        intent_score=state["intent_score"],
    )

    return {
        "prediction": prediction,
    }

async def assess_risk(
    state: IntelligenceState,
    risk_assessment_service: RiskAssessmentService,
    risk_signal_adapter: RiskSignalAdapter,
) -> dict:

    property_characteristics = {}

    property_profile = state.get(
        "property_profile",
    )

    if property_profile is not None:
        property_characteristics = {
            "year_built": str(
                property_profile.year_built
            )
        } if property_profile.year_built is not None else {}

    environmental_observations = {}

    observation = state.get(
        "environmental_observation",
    )

    if observation is not None:
        environmental_observations = {
            "rainfall": str(
                observation.rainfall_mm
            ),
            "temperature": str(
                observation.temperature_c
            ),
            "humidity": str(
                observation.humidity_percent
            ),
            "wind_speed": str(
                observation.wind_speed_mps
            ),
            "frost": str(
                observation.frost
            ),
        }

    assessment = (
        await risk_assessment_service.assess(
            risk_types=[
                "pest",
                "flood",
            ],
            property_characteristics=(
                property_characteristics
            ),
            environmental_observations=(
                environmental_observations
            ),
        )
    )

    risk_signals = (
        risk_signal_adapter.to_signals(
            assessment,
        )
    )

    return {
        "risk_assessment": assessment,
        "risk_signals": risk_signals,
    }