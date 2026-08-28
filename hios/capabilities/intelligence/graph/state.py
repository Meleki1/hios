from typing import TypedDict
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.intelligence.models.prediction import Prediction
from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation
from hios.capabilities.property.models.property_profile import PropertyProfile
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.risk.models.risk_assessment import RiskAssessment
from hios.capabilities.local_activity.models.provider_result import LocalActivityProviderResult
from hios.capabilities.timeline.models.timeline_entry import TimelineEntry


class IntelligenceState(TypedDict, total=False):

    subject_id: str
    target: str
    horizon_days: int

    property_profile: PropertyProfile | None

    environmental_observation: (
        EnvironmentalObservation | None
    )

    explicit_intents: list[str]
    interactions: list[str]

    timeline: list[TimelineEntry]

    risk_assessment: RiskAssessment | None
    risk_signals: list[Signal]
    
    local_activities: dict[str, str]
    
    local_activity_provider_results: list[
        LocalActivityProviderResult
    ]

    platform_behaviours: dict[str, str]

    intent_score: IntentScore | None

    prediction: Prediction | None
    

    