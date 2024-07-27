from enum import Enum, auto


class ColorMode(Enum):
    """Style for displaying the snake in the user interface."""
    SOLID = auto()
    PATTERN_ONCE = auto()
    PATTERN_REPEAT = auto()
