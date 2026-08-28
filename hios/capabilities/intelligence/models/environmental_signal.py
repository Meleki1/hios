from enum import Enum


class EnvironmentalSignal(str, Enum):
    RAINFALL = "rainfall"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    FROST = "frost"
    WIND = "wind"
    SEASONALITY = "seasonality"