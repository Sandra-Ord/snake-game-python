class Food:
    """
    Snake Food class.

    Food is an element in the snake game, which appears in random locations on the game board.
    Snake has to make its way to the food and upon eating, the snake gains points equal to the food's score points.
    """

    def __init__(self, x_coordinate: int, y_coordinate: int, score: int = 1, lifetime: int = None):
        """
        Food constructor method.

        Coordinates define the top left corner of the food block and
        blocks defines the amount of game blocks the food is wide and high from that point (1x1 block).
        Food should always be square-like (corners can be rounded for displaying).

        :param x_coordinate: Food block's left edge x-coordinate measured in game blocks.
        :param y_coordinate: Food block's top edge y-coordinate measured in game blocks.
        :param score: The amount of points, the snake gains for eating the food. Allows "superfoods" to be generated.
        :param lifetime: The amount of steps, that the snake can take, until the food will disappear.
                         If set to None (default), the food will remain on the board indefinitely.
                         If set to a number, with each snake step, the number is decreased until it reaches 0,
                         then new food will be generated.
                         This can be used, to create super foods which are worth more points,
                         but will disappear after some time.
        """
        self.score = score
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.blocks = 1
        self.lifetime = lifetime

    def decrease_lifetime(self) -> None:
        """Decrease the lifetime, if it has been set."""
        if self.lifetime is not None and self.lifetime > 0:
            self.lifetime -= 1
