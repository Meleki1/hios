import pytest

from hios.capabilities.risk.models.risk_score import (
    RiskLevel,
    RiskScore,
)
from hios.capabilities.risk.risk_service import (
    RiskService,
)


class FakeRiskEngine:

    def __init__(self):
        self.received = None

    async def assess(
        self,
        **kwargs,
    ) -> RiskScore:

        self.received = kwargs

        return RiskScore(
            risk_type=kwargs["risk_type"],
            score=65.0,
            level=RiskLevel.MEDIUM,
            confidence=0.9,
        )


@pytest.mark.asyncio
async def test_risk_service_delegates_to_engine():

    engine = FakeRiskEngine()

    service = RiskService(
        engine=engine,
    )

    result = await service.assess(
        risk_type="pest",
        property_characteristics={
            "year_built": "1890",
        },
        environmental_observations={
            "rainfall": "42.0",
        },
    )

    assert result.risk_type == "pest"
    assert result.score == 65.0
    assert result.level == RiskLevel.MEDIUM

    assert (
        engine.received["risk_type"]
        == "pest"
    )

    assert (
        engine.received["property_characteristics"]
        == {"year_built": "1890"}
    )

    assert (
        engine.received["environmental_observations"]
        == {"rainfall": "42.0"}
    )