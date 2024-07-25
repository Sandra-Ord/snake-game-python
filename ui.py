from brain import Brain
import colors
import pygame
from score_type import ScoreType


class Ui:
    """
    Ui class handles displaying the game elements in the desired scale.

    The game brain describes the elements' locations in in-game blocks as the game is supposed to be pixelated.
    Ui class converts the block measurements to pixels, using the block_size to scale blocks to the wished scale.
    """

    # todo implement different color schemas ?
    # green snake and red food is default classic
    # can create color package classes with different implementation
    # (snake_head color, snake body color, text color, background color etc for customization)
    def __init__(self, brain: Brain, block_size=10):
        self.brain = brain

        self.block_size = block_size  # How many pixels is one in-game block

        self.display_width = self.blocks_to_pixels(brain.display_width)  # Actual width of the game board
        self.display_height = self.blocks_to_pixels(brain.display_height)  # Actual height of the game board

        self.display = pygame.display.set_mode([self.display_width, self.display_height])

        self.game_font = pygame.font.SysFont(None, 25)

    def blocks_to_pixels(self, blocks: int) -> int:
        """
        Converts the in-game block measurements to pixel measurements for the display.
        Multiplies the number of blocks with the block_size.

        :param blocks: Coordinate or measurement size in in-game blocks.
        :return: Block measurement converted to pixels.
        """
        return blocks * self.block_size

    def pixel_rectangle(self, block_rectangle):
        """
        Converts the rectangle in-game block measurement information list to pixel information.

        :param block_rectangle: Rectangle information [left_x_coordinate, top_y_coordinate, width, height]
                                measured in in-game blocks.
        :return: Rectangle information [left_x_coordinate, top_y_coordinate, width, height] measured in pixels.
        """
        return [self.blocks_to_pixels(value) for value in block_rectangle]

    def draw_game_area(self, base_color=colors.BLACK, border_color=colors.WHITE) -> None:
        """
        Draws the base of the game board and surrounds it with the game's borders.

        :param base_color: Color of the game board background.
        :param border_color: Color of the borders.
        """
        self.display.fill(base_color)
        for border in self.brain.get_borders():
            pygame.draw.rect(self.display, border_color, self.pixel_rectangle(border))

    def draw_snake(self, color=colors.GREEN):
        """
        Draws the snake block by block.

        :param color: Color of the snake's body.
        """
        for pos in self.brain.snake.positions:
            pygame.draw.rect(self.display, color, self.pixel_rectangle([pos[0], pos[1], 1, 1]))

    def draw_food(self, color=colors.RED):
        """
        Draws the food block.

        :param color: Color of the food block.
        """
        food_x, food_y = self.brain.food.x_coordinate, self.brain.food.y_coordinate
        pygame.draw.rect(self.display, color, self.pixel_rectangle([food_x, food_y, 1, 1]))

    def display_score(self, score_type=ScoreType.Current, x=0, y=0, score_tag_text="", color=colors.RED):
        """
        Displays the desired score (current or high score) at the given coordinates with the tag text in front.

        :param score_type: Score type to define which score to use with the text (current or high).
        :param x: X-coordinate of the text.
        :param y: Y-coordinate of the text.
        :param score_tag_text: Text to write in front of the score, to identify which score it is (e.g. Highscore: 21).
        :param color: Color of the text.
        """
        score = self.brain.high_score if score_type is ScoreType.High else self.brain.current_score
        text = self.game_font.render(score_tag_text + str(score), True, color)
        self.display.blit(text, [x, y])

    def display_game_status(self, color=colors.WHITE):
        if self.brain.game_paused:
            status_text = "Game Over" if self.brain.game_over else "Game Paused"
            text = self.game_font.render(status_text, True, color)
            self.display.blit(text, [self.display_width / 2, self.display_height / 3])
