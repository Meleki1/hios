from hios.capabilities.environmental.service import EnvironmentalService
from hios.capabilities.environmental.graph.state import EnvironmentalState
from hios.capabilities.environmental.signal_collector import EnvironmentalSignalCollector


async def collect_environmental_data(
    state: EnvironmentalState,
    environmental_service: EnvironmentalService,
) -> dict:

    latitude = state["latitude"]
    longitude = state["longitude"]

    observation = await environmental_service.get_observation(
        latitude=latitude,
        longitude=longitude,
    )

    return {
        "environmental_observation": observation,
    }

async def produce_environmental_signals(
    state: EnvironmentalState,
    collector: EnvironmentalSignalCollector,
) -> dict:

    observation = state.get(
        "environmental_observation"
    )

    if observation is None:
        return {
            "environmental_signals": [],
        }

    signals = await collector.collect(
        observation,
    )

    return {
        "environmental_signals": signals,
    }