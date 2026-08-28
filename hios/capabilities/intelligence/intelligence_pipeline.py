from hios.capabilities.intelligence.models.prediction import Prediction


class IntelligencePipeline:

    def __init__(
        self,
        signal_collection_service,
        intelligence_service,
    ):
        self._signal_collection_service = (
            signal_collection_service
        )
        self._intelligence_service = (
            intelligence_service
        )

    async def predict(
        self,
        subject_id: str,
        target: str,
        horizon_days: int,
        property_profile=None,
        environmental_observation=None,
        explicit_intents=None,
        interactions=None,
        local_activities=None,
        platform_behaviours=None,
    ) -> Prediction:

        intent_score = (
            await self._signal_collection_service.collect_and_score(
                subject_id=subject_id,
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

        return await self._intelligence_service.predict(
            subject_id=subject_id,
            target=target,
            horizon_days=horizon_days,
            intent_score=intent_score,
        )