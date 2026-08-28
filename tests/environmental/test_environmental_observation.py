from hios.capabilities.environmental.models.environmental_observation import (
    EnvironmentalObservation,
)


def test_environmental_observation_can_be_created():

    observation = EnvironmentalObservation(
        rainfall_mm=42.0,
        temperature_c=18.5,
        humidity_percent=78.0,
        wind_speed_mps=4.2,
        frost=False,
    )

    assert observation.rainfall_mm == 42.0
    assert observation.temperature_c == 18.5
    assert observation.humidity_percent == 78.0
    assert observation.wind_speed_mps == 4.2
    assert observation.frost is False