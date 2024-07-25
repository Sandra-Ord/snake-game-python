import random

from enums.game_status import GameStatus
from snake import Snake
from food import Food


class Brain:
    """
    Game brain class to store game elements, game state and other related information.

    Game consists of:
        * a play area, which is surrounded by a border,
        * a snake, who is supposed to move around and avoid the border and its own tail,
        * snake foods, which appears one at a time (typically after the previous one has been eaten by the snake).

    The brain stores:
        * game board measurements,
        * snake information and location,
        * food information and location,
        * game status,
        * current score,
        * a high score, which is stored for the time the game is open.

    The game brain's area of responsibility is to describe the elements' locations in in-game blocks
    (the game is intended to be pixelated).
    """

    def __init__(self, game_area_width: int, game_area_height: int, border_widths: list[int]):
        """
        Game Brain constructor method.

        :param game_area_width: The total amount of in-game blocks that the game area is wide (borders excluded).
        :param game_area_height: The total amount of in-game block that the game area is high (borders excluded).
        :param border_widths: The width of the border measured in in-game blocks.
                              Widths for borders are taken in the following order: [top, bottom, left, right],
                              all missing values default to 2.
        """
        border_widths = (border_widths + [2] * 4)[:4]  # Fill the missing positions with the default value 2
        self.top_border, self.bottom_border, self.left_border, self.right_border = border_widths

        self.game_area_width = game_area_width
        self.game_area_height = game_area_height

        self.display_width = self.left_border + game_area_width + self.right_border  # total width of the display
        self.display_height = self.top_border + game_area_height + self.bottom_border  # total height of the display

        if self.game_area_width < 2 or self.game_area_height < 2:
            raise ValueError("Game field area is too small, there must be at least 2x2 blocks inside the borders.")

        self.game_paused = True
        self.game_status = GameStatus.ONGOING
        self.game_quit = False

        self.current_score = 0  # Points collected during the current game
        self.high_score = 0  # Highest number of points collected during the current session

        self.snake = self.new_snake()
        self.food = self.generate_food()

    def new_snake(self) -> Snake:
        """Create a new snake that will start in the center of the game board, moving in a random direction."""
        return Snake(self.display_width // 2, self.display_height // 2)

    def snake_at_max_capacity(self) -> bool:
        """Check if the snake has reached the maximum capacity of the game board."""
        return self.snake.length() >= self.game_area_width * self.game_area_height

    def reset_score(self) -> None:
        """Set the current_score to 0 points."""
        self.current_score = 0

    def set_high_score(self) -> None:
        """Take the maximum value between the current_score and high_score and assigns it as the new high score."""
        self.high_score = max(self.current_score, self.high_score)

    def pause_game(self) -> None:
        """Set the game_paused value to True."""
        self.game_paused = True

    def unpause_game(self) -> None:
        """
        Set the game_paused value to False.

        NB! Game can't be un-paused, if it is not ongoing.
        """
        if not self.game_in_play():
            return
        self.game_paused = False

    def start_game(self) -> None:
        """Set the game_status to Ongoing."""
        self.game_status = GameStatus.ONGOING

    def end_game(self) -> None:
        """
        Change the game status to Lost or Won.

        The Snake Game can be won, if the snake reaches the game area's maximum capacity.
        """
        if self.snake_at_max_capacity():
            self.game_status = GameStatus.WON
        else:
            self.game_status = GameStatus.LOST

    def quit_game(self) -> None:
        """Set the game_quit value to True."""
        self.game_quit = True

    def game_lost(self) -> bool:
        """Check if the game has been lost (game is not ongoing, and it has not been won either)?"""
        return self.game_status == GameStatus.LOST

    def game_won(self) -> bool:
        """Check if the game has been won (game is not ongoing, and it has not been lost either)?"""
        return self.game_status == GameStatus.WON

    def game_in_play(self) -> bool:
        """
        Check if the game is currently in play.

        :return: True, if the game is currently ongoing.
                 False, if the game has ended and has a result (lost/won).
        """
        return self.game_status == GameStatus.ONGOING

    def get_borders(self) -> list[list[int, int, int, int]]:
        """
        List of border rectangles.

        :return: List of border rectangle information [x, y, width, height] in the order [top, bottom, left, right].
        """
        return [[0, 0, self.display_width, self.top_border],
                [0, self.display_height - self.bottom_border, self.display_width, self.bottom_border],
                [0, 0, self.left_border, self.display_height],
                [self.display_width - self.right_border, 0, self.right_border, self.display_height]]

    def generate_food(self) -> Food:
        """
        Generate a new food in a random location on the game board and assign it as the game's current food.
        Location is generated randomly and checked to ensure, that it was not generated under the snake's positions.

        :return: Generated food object.
        """
        # todo leave out the snake's positions from the random generation.
        self.food = Food(random.randrange(0 + self.left_border, self.display_width - self.right_border, 1),
                         random.randrange(0 + self.top_border, self.display_height - self.bottom_border, 1))
        return self.food

    def snake_collision_detection(self) -> bool:
        """
        Detect if the snake incurred a collision (either with itself or with a border).

        :return: Boolean value to represent if the snake head collided into a border or itself.
        """
        return self.snake_border_collision() or self.snake.self_collision_detection()

    def snake_border_collision(self) -> bool:
        """
        Detect if the snake's head collided with any of the borders.

        Snake can touch the border and move against it, but can't go any further as that is considered a collision.

        :return: Boolean value to represent if a border collision incurred.
        """
        head_x, head_y = self.snake.body_positions[0]
        return (head_x < 0 + self.left_border or
                head_x >= self.display_width - self.right_border or
                head_y < 0 + self.top_border or
                head_y >= self.display_height - self.bottom_border)

    def snake_eating_detection(self) -> bool:
        """
        Check if the snake's head's position matches the food's position.

        :return: Boolean for whether the snake reached the food.
        """
        return self.snake.body_positions[0] == (self.food.x_coordinate, self.food.y_coordinate)

    def snake_eat(self) -> None:
        """Grow the snake and add the food's score points to the current score."""
        # todo should the previous food be set to None?
        self.snake.grow()
        self.current_score += self.food.score

    def finish_game(self) -> None:
        """Pause and end the current game."""
        self.pause_game()
        self.end_game()

    def restart_game(self) -> None:
        """
        Start a new game.

        Finish up the previous game round by updating the high score, if necessary and
        reset the score for the new game.
        Create a new snake, that will start from the middle of the board in a random direction.
        Pause the game, to prevent the next game from playing straight away.
        """
        self.set_high_score()
        self.reset_score()
        self.snake = self.new_snake()
        self.pause_game()
        self.start_game()
