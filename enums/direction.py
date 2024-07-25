from enum import Enum, auto


class Direction(Enum):
    """Direction of the snake's movement in the game area."""
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()
