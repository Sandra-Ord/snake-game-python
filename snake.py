from direction import Direction


class Snake:
    """
    Snake class to store snake's data and to interact with the snake.

    Snake is an element in the snake game, whose mission is to eat food, gain points and grow longer.

    The snake starts out as a block sized object who can move around and
    who has to make its way towards the Food objects in the game.
    The snake should avoid colliding into its own tail or the game worlds borders as that ends the game.
    """

    def __init__(self, left: int, top: int, block_size=10, step=10, direction=Direction.RIGHT):
        """
        Snake constructor method.

        :param left: Snake block's left edge x-coordinate measured in game blocks.
        :param top: Snake block's top edge y-coordinate measured in game blocks.
        :param block_size:
        :param step: Defines how big of a movement snake's one step is.
        :param direction: Snake's starting direction
        todo make into blck measurements and make static method for random coordinates and direction (goes is game brain)
        """
        self.positions = [(left, top)]

        self.block_size = block_size
        self.step = step
        self.direction = direction

        self.length = 1

    def change_direction(self, new_direction: Direction) -> None:
        """
        If the snake is 1 block long, then the snake can turn to any direction.
        If the snake is any longer, then the snake can turn
            to any directions that is not the opposite of the previous direction,
            as that would result in the snake turning into itself.
        :param new_direction: direction the snake will turn to and keep moving in.
        :return: None
        """
        turn_allowed = [new_direction == Direction.RIGHT and not self.direction == Direction.LEFT,
                        new_direction == Direction.LEFT and not self.direction == Direction.RIGHT,
                        new_direction == Direction.UP and not self.direction == Direction.DOWN,
                        new_direction == Direction.DOWN and not self.direction == Direction.UP]
        if self.length == 1 or any(turn_allowed):
            self.direction = new_direction

    def move(self) -> None:
        """
        Get the snake's head's current coordinates.
        Shift the coordinates by the snake's speed (step).
        Add the new head position to the beginning of the snake's positions list and
        remove the last element from snake's tail.
        :return: None
        """
        head_x, head_y = self.positions[0]
        new_head_position = self.shift_head_coordinates(head_x, head_y)
        self.positions = [new_head_position] + self.positions[:-1]

    def grow(self) -> None:
        self.length += 1
        self.positions.append(self.positions[-1])

    def shift_head_coordinates(self, head_x, head_y) -> (int, int):
        """
        Shifts the snakes head's coordinates by the step.

        :param head_x: Snake's head current x-coordinate.
        :param head_y: Snake's head current y-coordinate.
        :return: Snake's head's new coordinates.
        """
        if self.direction == Direction.RIGHT:
            head_x += self.step
        if self.direction == Direction.LEFT:
            head_x -= self.step
        if self.direction == Direction.UP:
            head_y -= self.step
        if self.direction == Direction.DOWN:
            head_y += self.block_size
        return head_x, head_y

    def self_collision_detection(self) -> bool:
        """
        Detects if the snake has collided into itself.
        :return: Boolean for whether there has been a collision.
        """
        for segment in self.positions[1:]:
            if segment == self.positions[0]:
                return True
        return False
