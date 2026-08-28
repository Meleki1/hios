from hios.capabilities.risk.models.risk_assessment import (
    RiskAssessment,
)
from hios.capabilities.risk.risk_service import (
    RiskService,
)


class RiskAssessmentService:

    def __init__(
        self,
        risk_service: RiskService,
    ):
        self._risk_service = risk_service

    async def assess(
        self,
        risk_types: list[str],
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
    ) -> RiskAssessment:

        risks = []

        for risk_type in risk_types:

            risk = await self._risk_service.assess(
                risk_type=risk_type,
                property_characteristics=(
                    property_characteristics
                ),
                environmental_observations=(
                    environmental_observations
                ),
            )

            risks.append(risk)

        return RiskAssessment(
            risks=risks,
        )