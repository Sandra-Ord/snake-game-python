from enum import Enum, auto


class ColorMode(Enum):
    """Style for displaying the snake in the user interface."""
    SOLID = auto()
    STRIPED = auto()
    DIFFERENT_HEAD = auto()
    DIFFERENT_TAIL = auto()
