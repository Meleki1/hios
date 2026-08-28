from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentalObservation:

    rainfall_mm: float | None = None
    temperature_c: float | None = None
    humidity_percent: float | None = None
    wind_speed_mps: float | None = None
    frost: bool | None = None