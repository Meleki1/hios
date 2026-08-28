from datetime import datetime
from hios.capabilities.intelligence.basic_signal_engine import BasicSignalEngine
from hios.capabilities.intelligence.models.signal import Signal
from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation
from hios.capabilities.environmental.service import EnvironmentalService
from hios.capabilities.property.models.property_profile import PropertyProfile
from hios.capabilities.property.service import PropertyService
from hios.capabilities.intelligence.intent_scorer import IntentScorer
from hios.capabilities.intelligence.models.intent_score import IntentScore
from hios.capabilities.local_activity.local_activity_service import LocalActivityService
from hios.capabilities.intelligence.collectors.local_activity import LocalActivitySignalCollector
from hios.capabilities.local_activity.local_activity_aggregator import LocalActivityAggregator
from hios.capabilities.local_activity.models.local_activity_event import LocalActivityEvent
from hios.capabilities.local_activity.models.provider_result import LocalActivityProviderResult
from hios.capabilities.image_diagnosis.models.image_diagnosis import ImageDiagnosis
from hios.capabilities.image_diagnosis.services.image_signal_collector import ImageSignalCollector


class SignalCollectionService:

    def __init__(
        self,
        signal_engine: BasicSignalEngine,
        intent_scorer: IntentScorer,
        property_service: PropertyService,
        environmental_service: EnvironmentalService,
        local_activity_service: LocalActivityService,
        local_activity_aggregator: LocalActivityAggregator,
        local_activity_signal_collector: LocalActivitySignalCollector,
        image_signal_collector: ImageSignalCollector | None = None,
    ):

        self._signal_engine = signal_engine
        self._intent_scorer = intent_scorer
        self._property_service = property_service
        self._environmental_service = (
            environmental_service
        )
        self._local_activity_service = (
            local_activity_service
        )

        self._local_activity_aggregator = (
            local_activity_aggregator
        )

        self._local_activity_signal_collector = (
            local_activity_signal_collector
        )
        self._image_signal_collector = (
            image_signal_collector
        )

    async def collect(
        self,
        subject_id: str,
        property_profile: PropertyProfile | None = None,
        environmental_observation: (
            EnvironmentalObservation | None
        ) = None,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
        radius_km: float = 5.0,
        include_local_activity: bool = True,
        image_diagnosis: ImageDiagnosis | None = None,
        image_home_id: str | None = None,
        image_observed_at: datetime | None = None,
    ) -> list[Signal]:

        property_characteristics = None

        if property_profile is not None:
            property_characteristics = (
                self._property_service.to_characteristics(
                    property_profile,
                )
            )

        environmental_observations = None

        if environmental_observation is not None:
            environmental_observations = (
                self._environmental_service.to_observations(
                    environmental_observation,
                )
            )

        # Collect the existing HIOS signals first.
        signals = await self._signal_engine.collect(
            subject_id=subject_id,
            explicit_intents=explicit_intents,
            interactions=interactions,
            property_characteristics=(
                property_characteristics
            ),
            environmental_observations=(
                environmental_observations
            ),
            local_activities=local_activities,
            platform_behaviours=platform_behaviours,
        )

        # Automatically collect area-level local activity
        # when the property has coordinates.
        if (
            include_local_activity
            and property_profile is not None
            and property_profile.latitude is not None
            and property_profile.longitude is not None
        ):

            (
                local_activity_signals,
                _,
            ) = await (
                self.collect_local_activity_with_status(
                    subject_id=subject_id,
                    property_profile=(
                        property_profile
                    ),
                    radius_km=radius_km,
                )
            )

            signals.extend(
                local_activity_signals
            )

        if (
            image_diagnosis is not None
            and self._image_signal_collector is not None
        ):
            if image_home_id is None:
                raise ValueError(
                    "image_home_id is required when "
                    "image_diagnosis is provided."
                )

            if image_observed_at is None:
                raise ValueError(
                    "image_observed_at is required when "
                    "image_diagnosis is provided."
                )

            image_signals = (
                self._image_signal_collector.collect(
                    subject_id=subject_id,
                    home_id=image_home_id,
                    diagnosis=image_diagnosis,
                    observed_at=image_observed_at,
                )
            )

            signals.extend(image_signals)

        return signals

    async def collect_local_activity_with_status(
        self,
        subject_id: str,
        property_profile: PropertyProfile,
        radius_km: float = 5.0,
    ) -> tuple[
        list[Signal],
        list[LocalActivityProviderResult],
    ]:

        if (
            property_profile.latitude is None
            or property_profile.longitude is None
        ):
            return [], []

        provider_results = (
            await self._local_activity_service.get_events_with_status(
                latitude=property_profile.latitude,
                longitude=property_profile.longitude,
                radius_km=radius_km,
            )
        )

        events: list[LocalActivityEvent] = []

        for result in provider_results:
            events.extend(result.events)

        trends = (
            self._local_activity_aggregator.aggregate(
                events,
            )
        )

        local_activity_signals = (
            await self._local_activity_signal_collector.collect_trends(
                subject_id=subject_id,
                trends=trends,
            )
        )

        return (
            local_activity_signals,
            provider_results,
        )

    async def collect_and_score(
        self,
        subject_id: str,
        property_profile: PropertyProfile | None = None,
        environmental_observation: (
            EnvironmentalObservation | None
        ) = None,
        explicit_intents: list[str] | None = None,
        interactions: list[str] | None = None,
        local_activities: dict[str, str] | None = None,
        platform_behaviours: dict[str, str] | None = None,
        radius_km: float = 5.0,
    ) -> IntentScore:

        signals = await self.collect(
            subject_id=subject_id,
            property_profile=property_profile,
            environmental_observation=environmental_observation,
            explicit_intents=explicit_intents,
            interactions=interactions,
            local_activities=local_activities,
            platform_behaviours=platform_behaviours,
            radius_km=radius_km,
        )

        return await self._intent_scorer.score(
            signals,
        )

    async def score_signals(
        self,
        signals: list[Signal],
    ) -> IntentScore:

        return await self._intent_scorer.score(
            signals,
        )