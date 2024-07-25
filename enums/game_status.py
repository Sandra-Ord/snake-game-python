from enum import Enum


class GameStatus(Enum):
    """
    Status of the game.

    Define if the game currently in play (Ongoing)
    or if it has ended and has a result (Lost/Won).
    """
    LOST = -1
    ONGOING = 0
    WON = 1
