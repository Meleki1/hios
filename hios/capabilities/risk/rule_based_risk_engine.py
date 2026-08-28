from hios.capabilities.risk.models.risk_score import (
    RiskLevel,
    RiskScore,
)
from hios.capabilities.risk.risk_engine import RiskEngine


class RuleBasedRiskEngine(RiskEngine):

    async def assess(
        self,
        risk_type: str,
        property_characteristics: dict[str, str] | None = None,
        environmental_observations: dict[str, str] | None = None,
    ) -> RiskScore:

        property_characteristics = (
            property_characteristics or {}
        )

        environmental_observations = (
            environmental_observations or {}
        )

        score = 0.0

        if risk_type == "flood":
            score = self._assess_flood(
                property_characteristics,
                environmental_observations,
            )

        elif risk_type == "pest":
            score = self._assess_pest(
                property_characteristics,
                environmental_observations,
            )

        score = min(score, 100.0)

        if score >= 70:
            level = RiskLevel.HIGH
        elif score >= 40:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        return RiskScore(
            risk_type=risk_type,
            score=score,
            level=level,
            confidence=1.0,
        )

    def _assess_flood(
        self,
        property_characteristics: dict[str, str],
        environmental_observations: dict[str, str],
    ) -> float:

        score = 0.0

        flood_risk = property_characteristics.get(
            "flood_risk",
        )

        if flood_risk == "high":
            score += 70.0
        elif flood_risk == "medium":
            score += 40.0
        elif flood_risk == "low":
            score += 10.0

        return score

    def _assess_pest(
        self,
        property_characteristics: dict[str, str],
        environmental_observations: dict[str, str],
    ) -> float:

        score = 0.0

        rainfall = environmental_observations.get(
            "rainfall",
        )

        if rainfall is not None:
            rainfall_value = float(rainfall)

            if rainfall_value >= 50:
                score += 30.0
            elif rainfall_value >= 25:
                score += 15.0

        return score