import pytest
from hios.capabilities.environmental.graph.nodes import collect_environmental_data
from hios.capabilities.environmental.graph.state import EnvironmentalState
from hios.capabilities.environmental.providers.mock import MockEnvironmentalProvider
from hios.capabilities.environmental.service import EnvironmentalService
from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation
from hios.capabilities.environmental.signal_collector import EnvironmentalSignalCollector
from hios.capabilities.intelligence.models.signal_type import SignalType
from hios.capabilities.environmental.graph.nodes import produce_environmental_signals
from hios.capabilities.environmental.graph.workflow import build_environmental_graph


@pytest.mark.asyncio
async def test_collect_environmental_data_node():

    service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    state: EnvironmentalState = {
        "latitude": 51.5074,
        "longitude": -0.1278,
    }

    result = await collect_environmental_data(
        state=state,
        environmental_service=service,
    )

    observation = result[
        "environmental_observation"
    ]

    assert observation is not None

    assert observation.rainfall_mm == 42.0
    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78.0
    assert observation.wind_speed_mps == 4.2
    assert observation.frost is False


@pytest.mark.asyncio
async def test_produce_environmental_signals_node():

    collector = EnvironmentalSignalCollector()

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    state: EnvironmentalState = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "environmental_observation": observation,
    }

    result = await produce_environmental_signals(
        state=state,
        collector=collector,
    )

    signals = result[
        "environmental_signals"
    ]

    assert len(signals) == 5

    assert all(
        signal.type == SignalType.ENVIRONMENTAL
        for signal in signals
    )




@pytest.mark.asyncio
async def test_environmental_graph_collects_and_produces_signals():

    environmental_service = EnvironmentalService(
        provider=MockEnvironmentalProvider(),
    )

    collector = EnvironmentalSignalCollector()

    graph = build_environmental_graph(
        environmental_service=environmental_service,
        collector=collector,
    )

    result = await graph.ainvoke(
        {
            "latitude": 51.5074,
            "longitude": -0.1278,
        }
    )

    observation = result[
        "environmental_observation"
    ]

    signals = result[
        "environmental_signals"
    ]

    assert observation is not None

    assert observation.rainfall_mm == 42.0
    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78.0

    assert len(signals) == 5

    signal_names = {
        signal.name
        for signal in signals
    }

    assert signal_names == {
        "rainfall",
        "temperature",
        "humidity",
        "wind_speed",
        "frost",
    }