from brain import Brain
import colors
import pygame
from enums.score_type import ScoreType


class Ui:
    """
    Ui class to display game elements in the desired scale.

    To display the game, convert the game brain's in-game block measurements to pixels,
    using the block_size to scale blocks to the wished scale.
    """

    # todo implement different color schemas ?
    # green snake and red food is default classic
    # can create color package classes with different implementation
    # (snake_head color, snake body color, text color, background color etc for customization)
    def __init__(self, brain: Brain, block_size=10):
        """
        Game Ui constructor method.

        :param brain: Game brain for which the ui is displayed.
        :param block_size: The amount of pixels that should be displayed per one in-game block.
        """
        self.brain = brain

        self.block_size = block_size

        self.display_width = self.blocks_to_pixels(brain.display_width)  # Actual width of the game board
        self.display_height = self.blocks_to_pixels(brain.display_height)  # Actual height of the game board

        self.display = pygame.display.set_mode([self.display_width, self.display_height])

        self.game_font = pygame.font.SysFont(None, 25)

    def draw_game(self) -> None:
        """
        Display the game screen.

        Elements that should be visible all the time:
            * game area with borders,
            * current score counter,
            * high score,
            * snake,
            * current food.

        If the game is paused,
        display the game status (paused/lost/won) and instructions.
        """
        self.draw_game_area()
        self.display_score(ScoreType.CURRENT)
        self.display_score(ScoreType.HIGH, round(self.display_width * 0.8), 0, "Highscore: ")
        self.draw_game_elements()
        if self.brain.game_paused:
            self.draw_pause_elements()

    def draw_game_elements(self) -> None:
        """Display the snake and the food."""
        self.draw_food()
        self.draw_snake()

    def draw_pause_elements(self) -> None:
        """Display the game status and brief instructions."""
        self.display_instructions()
        self.display_game_status()

    def draw_game_area(self, base_color=colors.BLACK, border_color=colors.WHITE) -> None:
        """
        Draw the base of the game board surrounded by the game's borders.

        :param base_color: Color of the game board background.
        :param border_color: Color of the borders.
        """
        self.display.fill(base_color)
        for border in self.brain.get_borders():
            pygame.draw.rect(self.display, border_color, self.pixel_rectangle(border))

    def draw_snake(self, color=colors.GREEN) -> None:
        """
        Draw the snake block by block.

        :param color: Color of the snake's body.
        """
        for pos in self.brain.snake.body_positions:
            pygame.draw.rect(self.display, color, self.pixel_rectangle([pos[0], pos[1], 1, 1]))

    def draw_food(self, color=colors.RED) -> None:
        """
        Draw the food block.

        :param color: Color of the food block.
        """
        food_x, food_y = self.brain.food.x_coordinate, self.brain.food.y_coordinate
        pygame.draw.rect(self.display, color, self.pixel_rectangle([food_x, food_y, 1, 1]))

    def display_score(self, score_type: ScoreType = ScoreType.CURRENT,
                      x: int = 0, y: int = 0,
                      score_tag_text: str = "", color=colors.RED) -> None:
        """
        Display the requested score (current or high score) at the given coordinates with the tag text in front.

        :param score_type: Score type to define which score to use with the text (current or high).
        :param x: X-coordinate of the text.
        :param y: Y-coordinate of the text.
        :param score_tag_text: Text to write in front of the score, to identify which score it is (e.g. Highscore: 21).
        :param color: Color of the text.
        """
        score = self.brain.high_score if score_type is ScoreType.HIGH else self.brain.current_score
        text = self.game_font.render(score_tag_text + str(score), True, color)
        self.display.blit(text, [x, y])

    def display_game_status(self, color=colors.WHITE) -> None:
        if self.brain.game_paused:
            status_text = ""
            if self.brain.game_in_play():
                status_text = "Game Paused"
            elif self.brain.game_lost():
                status_text = "Game Lost"
            elif self.brain.game_won():
                status_text = "Game Won"
            text = self.game_font.render(status_text, True, color)
            self.display.blit(text, [self.display_width / 2, self.display_height / 3])

    def display_instructions(self, color=colors.WHITE) -> None:
        # todo improve instructions
        instructions = [
            "Esc - Pause the Game",
            "Enter/Space - Continue",
            "S - Start a new Game",
            "Arrows - Move the Snake",
            "Q - Quit"
        ]
        line_height = self.display_height / 2
        for line in instructions:
            text = self.game_font.render(line, True, color)
            self.display.blit(text, [self.display_width / 2.5, line_height])
            line_height += 30

    # ----------------------------------------- HELPERS -----------------------------------------

    def blocks_to_pixels(self, blocks: int) -> int:
        """
        Convert the in-game block measurements to pixel measurements for the display.

        [Multiply the number of blocks with the block_size.]

        :param blocks: Coordinate or measurement size in in-game blocks.
        :return: Block measurement converted to pixels.
        """
        return blocks * self.block_size

    def pixel_rectangle(self, block_rectangle: list[int]) -> list[int]:
        """
        Convert the rectangle in-game block measurements list to pixel information.

        :param block_rectangle: Rectangle information [left_x_coordinate, top_y_coordinate, width, height]
                                measured in in-game blocks.
        :return: Rectangle information [left_x_coordinate, top_y_coordinate, width, height] measured in pixels.
        """
        return [self.blocks_to_pixels(value) for value in block_rectangle]
