from enum import Enum, auto


class ScoreType(Enum):
    """Score type, to increase code re-usage."""
    CURRENT = auto()
    HIGH = auto()
