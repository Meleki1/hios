from enum import Enum


class HomeType(str, Enum):

    RESIDENTIAL = "residential"

    COMMERCIAL = "commercial"

    INDUSTRIAL = "industrial"

    VACATION = "vacation"

    OFFICE = "office"

    SMART_HOME = "smart_home"

