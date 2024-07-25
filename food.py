class Food:
    """
    Snake Food class.

    Food is an element in the snake game, which appears in random locations on the game board.
    Snake has to make its way to the food and upon eating, the snake gains points equal to the food's score points.
    """

    def __init__(self, x_coordinate, y_coordinate, score=1, blocks=1):
        """
        Food constructor method.

        Coordinates define the top left corner of the food block and
        blocks defines the amount of game blocks the food is wide and high from that point.

        :param x_coordinate: Food block's left edge x-coordinate measured in game blocks.
        :param y_coordinate: Food block's top edge y-coordinate measured in game blocks.
        :param score: The amount of points, the snake gains for eating the food. Allows "superfoods" to be generated.
        :param blocks: Defines how many in-game game blocks should be the food's width and height (typically 1).
                        Food should always be square-like (corners can be rounded).
        """
        self.score = score
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.blocks = blocks


    # todo make static method to generate random coordinate food prbly static method should go in brain as here the width and height is not known