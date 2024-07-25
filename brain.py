import random
from snake import Snake
from food import Food


class Brain:
    """
    Game brain class to store game elements, game state and other related information.

    Brain consists of:
    * a play area, which is surrounded by a border,
    * a snake, who is supposed to move around and avoid the border and its own tail,
    * snake foods, which appears one at a time, after the previous one has been eaten by the snake.

    The brain holds the current score of the snake, which depends on the amount of food it has eaten,
    and a high score, which is stored for the time the game is open.
    """

    # todo implement game_win status
    # e.g. game_satus = -1, 0, 1
    # -1 - game lost | 0 - ongoing game | 1 - game won
    # game is won if the snake's length is equal to game_area_Width * game_area_height
    def __init__(self, game_area_width: int, game_area_height: int, border_widths):
        """
        Game Brain constructor method.

        :param game_area_width: The total amount of in-game blocks that the game area is wide (borders excluded).
        :param game_area_height: The total amount of in-game block that the game area is high (borders excluded).
        :param border_widths: The width of the border measured in in-game blocks.
                            If type is int - all borders take the same amount of blocks from the edge of the display.
                            If type is list - then widths for borders are taken as follows [top, bottom, left, right].
                                                if the list has fewer elements, the missing values default to 2.
        """
        if isinstance(border_widths, int):
            self.top_border = self.bottom_border = self.left_border = self.right_border = border_widths
        elif isinstance(border_widths, list):
            border_widths = (border_widths + [2] * 4)[:4]
            self.top_border, self.bottom_border, self.left_border, self.right_border = border_widths

        self.display_width = self.left_border + game_area_width + self.right_border  # total width of the display
        self.display_height = self.top_border + game_area_height + self.bottom_border  # total height of the display

        if (self.display_width < self.top_border + self.bottom_border + 2
                or self.display_height < self.left_border + self.right_border + 2):
            raise ValueError("Game field area is too small, there must be at least 2x2 blocks inside the borders.")

        self.game_paused = True  # game_active defines whether the game is currently in play or not
        self.game_over = False  # game_over defines if the game has been lost yet
        self.game_quit = False  # game_quit is a variable to stop the game_loop once the signal has been given

        self.current_score = 0  # Points collected during the current game
        self.high_score = 0  # Highest number of points collected during the current session

        self.snake = self.new_snake()
        self.food = self.generate_food()

    def new_snake(self) -> Snake:
        """Creates a new snake that will start in the center of the game board moving in a random direction."""
        return Snake(self.display_width // 2, self.display_height // 2)

    def reset_score(self):
        """Sets the current_score to 0 points."""
        self.current_score = 0

    def set_high_score(self):
        """Takes the maximum value for the current_score and high_score and assigns it as the new high score."""
        self.high_score = max(self.current_score, self.high_score)

    def pause_game(self):
        """Sets the game_paused value to True."""
        self.game_paused = True

    def unpause_game(self):
        """Sets the game_paused value to False."""
        if self.game_over:
            return
        self.game_paused = False

    def start_game(self):
        """Sets the game_over value to False."""
        self.game_over = False

    def end_game(self):
        """Sets the game_over value to True."""
        self.game_over = True

    def quit_game(self):
        """Sets the game_quit value to True."""
        self.game_quit = True

    def get_borders(self) -> []:
        """
        Gets a list of border rectangles.

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
        # maybe could be implemented with a list of all the game board block coordinates
        # from which the snakes position is subtracted
        self.food = Food(random.randrange(0 + self.left_border, self.display_width - self.right_border, 1),
                         random.randrange(0 + self.top_border, self.display_height - self.bottom_border, 1))
        return self.food

    def snake_collision_detection(self) -> bool:
        """
        Detects if the snake incurred a collision (either with itself or with a border).

        :return: Boolean value to represent if the snake head collided into a border or itself.
        """
        return self.snake_border_collision() or self.snake.self_collision_detection()

    def snake_border_collision(self) -> bool:
        """
        Detects if the snake's head collided with any of the borders.

        Snake can touch the border and move against it, but can't go any further as that is considered a collision.

        :return: Boolean value to represent if a border collision incurred.
        """
        head_x, head_y = self.snake.positions[0]
        return (head_x < 0 + self.left_border or
                head_x >= self.display_width - self.right_border or
                head_y < 0 + self.top_border or
                head_y >= self.display_height - self.bottom_border)

    def snake_eating_detection(self) -> bool:
        """
        Checks if the snake's head's position matches the food's position.

        :return: Boolean for whether the snake reached the food.
        """
        return self.snake.positions[0] == (self.food.x_coordinate, self.food.y_coordinate)

    def snake_eat(self):
        """Grow the snake and add the food's score points to the current score."""
        # todo should the previous food be set to None?
        self.snake.grow()
        self.current_score += self.food.score

    def game_lost(self):
        """Pause and end the current game."""
        self.pause_game()
        self.end_game()

    def restart_game(self):
        """
        Starts a new game.

        Finishes up the previous game round by updating the high score, if necessary and
        resets the score for the new game.
        Creates a new snake, that will start from the middle of the board in a random direction.
        Pauses the game, to stop the next game from playing straight away.
        """
        self.set_high_score()
        self.reset_score()
        self.snake = self.new_snake()
        self.pause_game()
        self.start_game()
