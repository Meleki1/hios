from hios.capabilities.risk.models.risk_score import RiskScore
from hios.capabilities.risk.risk_engine import RiskEngine


class RiskService:

    def __init__(
        self,
        engine: RiskEngine,
    ):
        self._engine = engine

    async def assess(
        self,
        risk_type: str,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
    ) -> RiskScore:

        return await self._engine.assess(
            risk_type=risk_type,
            property_characteristics=(
                property_characteristics
            ),
            environmental_observations=(
                environmental_observations
            ),
        )