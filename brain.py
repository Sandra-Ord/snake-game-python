import random
from snake import Snake
from food import Food


class Brain:

    def __init__(self, display_width, display_height, border_width):
        self.display_width = display_width
        self.display_height = display_height
        self.border_width = border_width

        self.game_paused = True  # game_active defines whether the game is currently in play or not
        self.game_over = False  # game_over defines if the game has been lost yet
        self.game_quit = False  # game_quit is a variable to stop the game_loop once the signal has been given

        self.current_score = 0
        self.high_score = 0

        self.snake = self.new_snake()
        self.food = self.generate_food()

    def new_snake(self) -> Snake:
        return Snake(self.display_width / 2, self.display_height / 2)

    def reset_score(self):
        self.current_score = 0

    def set_high_score(self):
        self.high_score = max(self.current_score, self.high_score)

    def pause_game(self):
        self.game_paused = True

    def unpause_game(self):
        self.game_paused = False

    def quit_game(self):
        self.game_quit = True

    def get_borders(self) -> [[int]]:
        """Returns a list of border rectangles [left, top, width, height] in the order: top, bottom, left, right."""
        return [[0, 0, self.display_width, self.border_width],
                [0, self.display_height - self.border_width, self.display_width, self.border_width],
                [0, 0, self.border_width, self.display_height],
                [self.display_width - self.border_width, 0, self.border_width, self.display_height]]

    def generate_food(self) -> Food:
        self.food = Food(round(random.randrange(0 + self.border_width, self.display_width - 2 * self.border_width) / 10.0) * 10.0,
                        round(random.randrange(0 + self.border_width, self.display_height - 2 * self.border_width) / 10.0) * 10.0)
        return self.food

    def snake_collision_detection(self) -> bool:
        """
        Detects if the snake incurred a collision (either with itself or with a border).
        Returns a boolean value to represent it (true - collision, false - no collision).
        """
        head_x, head_y = self.snake.positions[0]
        # Border Collision Detection
        if head_x < 0 + self.border_width \
                or head_x >= self.display_width - self.border_width \
                or head_y < 0 + self.border_width \
                or head_y >= self.display_height - self.border_width:
            return True
        # Snake's Self Collision Detection
        if self.snake.self_collision_detection():
            return True
        return False

    def snake_eating_detection(self) -> bool:
        return self.snake.positions[0] == (self.food.x_coordinate, self.food.y_coordinate)

    def snake_eat(self):
        self.snake.grow()
        self.current_score += 1

    def game_lost(self):
        self.pause_game()
        self.game_over = True

    def restart_game(self):
        self.set_high_score()
        self.reset_score()
        self.snake = self.new_snake()
        self.pause_game()
        self.game_over = False
