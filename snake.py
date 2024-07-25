import random

from enums.direction import Direction


class Snake:
    """
    Snake class to store snake's data and to interact with the snake.

    Snake is an element in the snake game, whose mission is to eat food, gain points and grow longer.

    The snake starts out as a block sized object who can move around and
    who has to make its way towards the Food objects in the game.
    The snake should avoid colliding into its own tail or the game worlds borders as that ends the game.
    """

    def __init__(self, left: int, top: int, step=1, direction=None):
        """
        Snake constructor method.

        :param left: Snake block's left edge x-coordinate measured in in-game blocks.
        :param top: Snake block's top edge y-coordinate measured in in-game blocks.
        :param step: Defines how many in-game blocks the snake should move forward at once.
        :param direction: Snake's starting direction.
                            If a direction is not provided, the snake will start in a random direction.
        """
        self.body_positions = [(left, top)]

        self.step = step

        if direction is None:
            direction = random.choice(list(Direction))
        self.direction = direction

    def length(self) -> int:
        """
        The length of the snake measured in in-game blocks.

        :return:Length of the snake
        """
        return len(self.body_positions)

    def change_direction(self, new_direction: Direction) -> None:
        """
        If the snake is 1 block long, then the snake can turn to any direction.
        If the snake is any longer, then the snake can turn
            to any directions that is not the opposite of the previous direction,
            as that would result in the snake turning into itself.

        :param new_direction: direction the snake will turn to and keep moving in.
        """
        opposite_directions = {
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
        }
        if self.length == 1 or self.direction != new_direction and new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def move(self) -> None:
        """
        Get the snake's head's current coordinates.
        Shift the coordinates by the snake's speed (step).
        Add the new head position to the beginning of the snake's body positions list and
        remove the last element from snake's tail.
        """
        head_x, head_y = self.body_positions[0]
        new_head_position = self.shift_head_coordinates(head_x, head_y)
        self.body_positions = [new_head_position] + self.body_positions[:-1]

    def grow(self) -> None:
        self.body_positions.append(self.body_positions[-1])

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
            head_y += self.step
        return head_x, head_y

    def self_collision_detection(self) -> bool:
        """
        Detects if the snake has collided into itself.

        :return: Boolean for whether there has been a collision.
        """
        for segment in self.body_positions[1:]:
            if segment == self.body_positions[0]:
                return True
        return False
