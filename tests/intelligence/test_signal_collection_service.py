import pytest

from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)
from hios.capabilities.environmental.providers.mock import (
    MockEnvironmentalProvider,
)
from hios.capabilities.environmental.service import (
    EnvironmentalService,
)
from hios.capabilities.intelligence.basic_signal_engine import (
    BasicSignalEngine,
)
from hios.capabilities.intelligence.collectors.conversation import (
    ConversationSignalCollector,
)
from hios.capabilities.intelligence.collectors.environmental import (
    EnvironmentalSignalCollector,
)
from hios.capabilities.intelligence.collectors.explicit_intent import (
    ExplicitIntentCollector,
)
from hios.capabilities.intelligence.collectors.local_activity import LocalActivitySignalCollector
from hios.capabilities.intelligence.collectors.platform import PlatformBehaviourSignalCollector
from hios.capabilities.intelligence.collectors.property import PropertySignalCollector
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.intelligence.signal_collection_service import SignalCollectionService
from hios.capabilities.property.providers.mock import MockPropertyProvider
from hios.capabilities.property.service import PropertyService
from hios.capabilities.intelligence.models.intent_level import IntentLevel
from hios.capabilities.intelligence.rule_based_intent_scorer import RuleBasedIntentScorer
from hios.capabilities.intelligence.intent_scorer import IntentScorer
from hios.capabilities.local_activity.local_activity_service import (
    LocalActivityService,
)

from hios.capabilities.local_activity.local_activity_aggregator import (
    LocalActivityAggregator,
)

from hios.capabilities.intelligence.collectors.local_activity import (
    LocalActivitySignalCollector,
)
from hios.capabilities.local_activity.providers.planning_applications import (
    MockPlanningApplicationProvider,
)
from datetime import datetime, timezone

from hios.capabilities.image_diagnosis.models.image_diagnosis import (
    ImageDiagnosis,
)
from hios.capabilities.image_diagnosis.models.image_finding import (
    ImageFinding,
)
from hios.capabilities.image_diagnosis.services.image_signal_collector import (
    ImageSignalCollector,
)
from hios.capabilities.intelligence.models.signal_source import (
    SignalSource,
)
from hios.capabilities.intelligence.models.signal_type import (
    SignalType,
)
from tests.intelligence.test_collector_intelligence_service import FakeIntentScorer
from hios.capabilities.intelligence.models.signal import Signal

class FakePropertyService:

    def __init__(
        self,
        *,
        characteristics: dict | None = None,
    ):
        self.characteristics = characteristics or {}
        self.calls: list = []

    def to_characteristics(
        self,
        property_profile,
    ) -> dict:

        self.calls.append(
            property_profile
        )

        return dict(self.characteristics)

class FakeEnvironmentalService:

    def __init__(
        self,
        *,
        observations: dict | None = None,
    ):
        self.observations = observations or {}
        self.calls: list = []

    def to_observations(
        self,
        environmental_observation,
    ) -> dict:

        self.calls.append(
            environmental_observation
        )

        return dict(self.observations)

class FakeLocalActivityService:

    def __init__(
        self,
        *,
        provider_results=None,
    ):
        self.provider_results = (
            provider_results or []
        )
        self.calls: list[dict] = []

    async def get_events_with_status(
        self,
        *,
        latitude: float,
        longitude: float,
        radius_km: float,
    ):

        self.calls.append(
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius_km": radius_km,
            }
        )

        return list(self.provider_results)


class FakeLocalActivityAggregator:

    def __init__(
        self,
        *,
        trends=None,
    ):
        self.trends = trends or []
        self.calls: list = []

    def aggregate(
        self,
        events,
    ):

        self.calls.append(
            events
        )

        return self.trends

class FakeLocalActivitySignalCollector:

    def __init__(
        self,
        *,
        signals: list[Signal] | None = None,
    ):
        self.signals = signals or []
        self.calls: list[dict] = []

    async def collect_trends(
        self,
        *,
        subject_id: str,
        trends,
    ) -> list[Signal]:

        self.calls.append(
            {
                "subject_id": subject_id,
                "trends": trends,
            }
        )

        return list(self.signals)

class FakeBasicSignalEngine:

    def __init__(
        self,
        *,
        signals: list[Signal] | None = None,
    ):
        self.signals = signals or []
        self.calls: list[dict] = []

    async def collect(
        self,
        *,
        subject_id: str,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        property_characteristics: dict | None = None,
        environmental_observations: dict | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
    ) -> list[Signal]:

        self.calls.append(
            {
                "subject_id": subject_id,
                "explicit_intents": explicit_intents,
                "interactions": interactions,
                "property_characteristics": (
                    property_characteristics
                ),
                "environmental_observations": (
                    environmental_observations
                ),
                "local_activities": local_activities,
                "platform_behaviours": platform_behaviours,
            }
        )

        return list(self.signals)

@pytest.mark.asyncio
async def test_signal_collection_service_collects_all_context():

    signal_engine = BasicSignalEngine(
        explicit_intent_collector=ExplicitIntentCollector(),
        conversation_collector=ConversationSignalCollector(),
        property_collector=PropertySignalCollector(),
        environmental_collector=EnvironmentalSignalCollector(),
        local_activity_collector=LocalActivitySignalCollector(),
        platform_behaviour_collector=(
            PlatformBehaviourSignalCollector()
        ),
    )

    property_service = PropertyService(
        provider=MockPropertyProvider(),
    )

    environmental_service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    local_activity_service = LocalActivityService(
        providers=[
            MockPlanningApplicationProvider(),
        ],
    )

    local_activity_aggregator = (
        LocalActivityAggregator()
    )

    local_activity_signal_collector = (
        LocalActivitySignalCollector()
    )

    intent_scorer = IntentScorer

    service = SignalCollectionService(
        signal_engine=signal_engine,
        intent_scorer=intent_scorer,
        property_service=property_service,
        environmental_service=environmental_service,
        local_activity_service=local_activity_service,
        local_activity_aggregator=local_activity_aggregator,
        local_activity_signal_collector=(
            local_activity_signal_collector
        ),
    )

    property_profile = await property_service.get_property(
        "100023456789",
    )

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    signals = await service.collect(
        subject_id="household-1",
        property_profile=property_profile,
        environmental_observation=observation,
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "asked_about_pests",
        ],
        local_activities={
            "local_pest_reports": "increasing",
        },
        platform_behaviours={
            "return_visits": "3",
        },
    )

    assert len(signals) > 6

    signal_types = {
        signal.type
        for signal in signals
    }

    assert signal_types == {
        SignalType.EXPLICIT_INTENT,
        SignalType.CONVERSATION,
        SignalType.PROPERTY,
        SignalType.ENVIRONMENTAL,
        SignalType.LOCAL_ACTIVITY,
        SignalType.PLATFORM_BEHAVIOUR,
    }

    property_signals = [
        signal
        for signal in signals
        if signal.type == SignalType.PROPERTY
    ]

    environmental_signals = [
        signal
        for signal in signals
        if signal.type == SignalType.ENVIRONMENTAL
    ]

    assert len(property_signals) > 1
    assert len(environmental_signals) == 5

    assert any(
        signal.name == "year_built"
        and signal.value == "1890"
        for signal in property_signals
    )

    assert any(
        signal.name == "epc_rating"
        and signal.value == "D"
        for signal in property_signals
    )

    assert any(
        signal.name == "rainfall_mm"
        and signal.value == "42.0"
        for signal in environmental_signals
    )

    assert any(
        signal.name == "temperature_c"
        and signal.value == "18.5"
        for signal in environmental_signals
    )

    assert any(
        signal.name == "humidity_percent"
        and signal.value == "78.0"
        for signal in environmental_signals
    )

    assert any(
        signal.name == "wind_speed_mps"
        and signal.value == "4.2"
        for signal in environmental_signals
    )

    assert any(
        signal.name == "frost"
        and signal.value == "False"
        for signal in environmental_signals
    )

@pytest.mark.asyncio
async def test_signal_collection_service_collects_and_scores():

    signal_engine = BasicSignalEngine(
        explicit_intent_collector=ExplicitIntentCollector(),
        conversation_collector=ConversationSignalCollector(),
        property_collector=PropertySignalCollector(),
        environmental_collector=EnvironmentalSignalCollector(),
        local_activity_collector=LocalActivitySignalCollector(),
        platform_behaviour_collector=(
            PlatformBehaviourSignalCollector()
        ),
    )

    property_service = PropertyService(
        provider=MockPropertyProvider(),
    )

    environmental_service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    local_activity_service = LocalActivityService(
        providers=[
            MockPlanningApplicationProvider(),
        ],
    )

    local_activity_aggregator = (
        LocalActivityAggregator()
    )

    local_activity_signal_collector = (
        LocalActivitySignalCollector()
    )

    scorer = RuleBasedIntentScorer()

    service = SignalCollectionService(
        signal_engine=signal_engine,
        intent_scorer=scorer,
        property_service=property_service,
        environmental_service=environmental_service,
        local_activity_service=local_activity_service,
        local_activity_aggregator=local_activity_aggregator,
        local_activity_signal_collector=(
            local_activity_signal_collector
        ),
    )

    property_profile = await property_service.get_property(
        "100023456789",
    )

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    result = await service.collect_and_score(
        subject_id="household-1",
        property_profile=property_profile,
        environmental_observation=observation,
        explicit_intents=[
            "reported_active_problem",
        ],
        interactions=[
            "asked_about_pests",
        ],
    )

    assert result.score == 25.0
    assert result.level == IntentLevel.LOW
    assert len(result.signals) > 0

    assert any(
        signal.value == "reported_active_problem"
        for signal in result.signals
    )

@pytest.mark.asyncio
async def test_signal_collection_includes_image_diagnosis_signals():

    diagnosis = ImageDiagnosis(
        findings=[
            ImageFinding(
                category="pest",
                description="Possible rodent evidence.",
                confidence=0.91,
                location="kitchen",
            ),
        ],
        overall_confidence=0.91,
    )

    image_signal_collector = ImageSignalCollector()

    service = SignalCollectionService(
        signal_engine=FakeBasicSignalEngine(),
        intent_scorer=FakeIntentScorer(),
        property_service=FakePropertyService(),
        environmental_service=FakeEnvironmentalService(),
        local_activity_service=FakeLocalActivityService(),
        local_activity_aggregator=FakeLocalActivityAggregator(),
        local_activity_signal_collector=(
            FakeLocalActivitySignalCollector()
        ),
        image_signal_collector=image_signal_collector,
    )

    signals = await service.collect(
        subject_id="household-1",
        image_diagnosis=diagnosis,
        image_home_id="home-1",
        image_observed_at=datetime(
            2026,
            8,
            22,
            tzinfo=timezone.utc,
        ),
        include_local_activity=False,
    )

    image_signals = [
        signal
        for signal in signals
        if signal.source is SignalSource.IMAGE
    ]

    assert len(image_signals) == 1

    signal = image_signals[0]

    assert signal.type is SignalType.IMAGE
    assert signal.source is SignalSource.IMAGE
    assert signal.name == "possible_pest_evidence"
    assert signal.value == (
        "Possible rodent evidence."
    )
    assert signal.confidence == 0.91
    assert signal.metadata["subject_id"] == "household-1"
    assert signal.metadata["home_id"] == "home-1"
    assert signal.metadata["location"] == "kitchen"