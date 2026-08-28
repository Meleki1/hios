from datetime import datetime, timedelta, timezone
from hios.capabilities.maintenance.models.maintenance_recommendation import (
    MaintenanceRecommendation,
)
from hios.capabilities.maintenance.models.maintenance import (
    Maintenance,
    MaintenanceStatus,
)
from hios.capabilities.maintenance.models.maintenance_intelligence_result import (
    MaintenanceIntelligenceResult,
)


class MaintenanceIntelligenceService:

    def __init__(
        self,
        intelligence_pipeline,
        history_extractor,
        pattern_detector,
        recommendation_scheduler,
        timeline_planner,
    ):
        self._intelligence_pipeline = intelligence_pipeline
        self._history_extractor = history_extractor
        self._pattern_detector = pattern_detector
        self._recommendation_scheduler = (
            recommendation_scheduler
        )
        self._timeline_planner = timeline_planner
    async def analyze(
        self,
        *,
        subject_id: str,
        home_id: str,
        timeline=None,
        maintenance_records=None,
        property_profile=None,
        environmental_observation=None,
        explicit_intents=None,
        interactions=None,
        local_activities=None,
        platform_behaviours=None,
    ):

        prediction = (
            await self._intelligence_pipeline.predict(
                subject_id=subject_id,
                target="home_maintenance",
                horizon_days=30,
                property_profile=property_profile,
                environmental_observation=(
                    environmental_observation
                ),
                explicit_intents=explicit_intents,
                interactions=interactions,
                local_activities=local_activities,
                platform_behaviours=platform_behaviours,
            )
        )

        history_signals = (
            self._history_extractor.extract(
                timeline or []
            )
        )

        patterns = (
            self._pattern_detector.detect(
                history_signals
            )
        )

        recommendations = self._build_recommendations(
            subject_id=subject_id,
            home_id=home_id,
            patterns=patterns,
            prediction=prediction,
            maintenance_records=(
                maintenance_records or []
            ),
        )

        timeline = await self._timeline_planner.build(
            subject_id=subject_id,
            home_id=home_id,
            maintenance_records=(
                maintenance_records or []
            ),
            recommendations=recommendations,
        )

        return MaintenanceIntelligenceResult(
            recommendations=recommendations,
            timeline=timeline,
        )

    def _build_recommendations(
        self,
        *,
        subject_id,
        home_id,
        patterns,
        prediction,
        maintenance_records,
    ):

        recommendations = []

        for pattern in patterns:
            if pattern.category == "pest":
                task = "Pest inspection"

                if not self._should_recommend(
                    home_id=home_id,
                    task=task,
                    maintenance_records=maintenance_records,
                    
                ):
                    continue

                recommended_for = (
                        self._recommendation_scheduler.schedule(
                            now=datetime.now(timezone.utc),
                            horizon_days=30,
                        )
                    )

                recommendations.append(
                    MaintenanceRecommendation(
                        subject_id=subject_id,
                        home_id=home_id,
                        task=task,
                        maintenance_type="preventive",
                        reason=(
                            "Repeated pest-related concerns "
                            "were identified in the home history."
                        ),
                        priority="normal",
                        recommended_for=recommended_for,
                        source_signals=pattern.descriptions,
                        metadata={
                            "pattern": pattern.category,
                            "occurrences": str(
                                pattern.occurrences
                            ),
                        },
                    )
                )
        return recommendations
    def _should_recommend(
        self,
        *,
        home_id: str,
        task: str,
        maintenance_records: list[Maintenance],
    ) -> bool:
        for record in maintenance_records:
            if record.home_id != home_id:
                continue

            if record.task != task:
                continue

            if record.status in (
                MaintenanceStatus.PLANNED,
                MaintenanceStatus.DUE,
                MaintenanceStatus.COMPLETED,
            ):
                return False

        return True

        