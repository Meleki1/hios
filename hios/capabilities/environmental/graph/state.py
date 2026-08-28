from typing import TypedDict

from hios.capabilities.environmental.models.environmental_observation import EnvironmentalObservation
from hios.capabilities.intelligence.models.signal import Signal

class EnvironmentalState(TypedDict, total=False):

    latitude: float
    longitude: float

    environmental_observation: EnvironmentalObservation
    environmental_signals: list[Signal]