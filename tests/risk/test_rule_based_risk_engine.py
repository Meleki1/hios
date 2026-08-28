import pytest

from hios.capabilities.risk.models.risk_score import (
    RiskLevel,
)
from hios.capabilities.risk.rule_based_risk_engine import (
    RuleBasedRiskEngine,
)


@pytest.mark.asyncio
async def test_high_flood_risk_produces_high_risk_score():

    engine = RuleBasedRiskEngine()

    result = await engine.assess(
        risk_type="flood",
        property_characteristics={
            "flood_risk": "high",
        },
    )

    assert result.risk_type == "flood"
    assert result.score == 70.0
    assert result.level == RiskLevel.HIGH


@pytest.mark.asyncio
async def test_heavy_rain_increases_pest_risk():

    engine = RuleBasedRiskEngine()

    result = await engine.assess(
        risk_type="pest",
        environmental_observations={
            "rainfall": "50",
        },
    )

    assert result.risk_type == "pest"
    assert result.score == 30.0
    assert result.level == RiskLevel.LOW


@pytest.mark.asyncio
async def test_unknown_risk_starts_at_zero():

    engine = RuleBasedRiskEngine()

    result = await engine.assess(
        risk_type="roof",
    )

    assert result.risk_type == "roof"
    assert result.score == 0.0
    assert result.level == RiskLevel.LOW