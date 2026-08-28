from enum import Enum

class HomeStatus(str, Enum):

    ACTIVE = "active"

    ARCHIVED = "archived"

    PENDING = "pending"