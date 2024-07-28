import pygame
from components.brain import Brain
from utils import colors
from enums.color_mode import ColorMode
from enums.game_status import GameStatus
from enums.score_type import ScoreType
from utils.color_scheme import ColorScheme


class Ui:
    """
    Ui class to display game elements in the desired scale.

    To display the game, convert the game brain's in-game block measurements to pixels,
    using the block_size to scale blocks to the wished scale.
    """

    def __init__(self, brain: Brain, block_size: int = 10):
        """
        Game Ui constructor method.

        :param brain: Game brain for which the ui is displayed.
        :param block_size: The amount of pixels that should be displayed per one in-game block.
        """
        self.brain = brain

        self.block_size = block_size

        self.color_scheme = ColorScheme.get_default_color_scheme()

        self.display_width = self.blocks_to_pixels(brain.display_width)  # Actual width of the game board
        self.display_height = self.blocks_to_pixels(brain.display_height)  # Actual height of the game board

        self.display = pygame.display.set_mode([self.display_width, self.display_height])

        self.score_font = pygame.font.SysFont("monospace", 20, True)
        self.instructions_font = pygame.font.SysFont("monospace", 18)
        self.game_font = pygame.font.SysFont("monospace", 25, True)

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
        self.display_score(ScoreType.CURRENT, self.blocks_to_pixels(self.brain.left_border))
        self.display_score(ScoreType.HIGH, round(self.display_width * 0.8), 0, "Highscore: ")
        self.display_scheme_name()
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

    def draw_snake(self) -> None:
        """Draw the snake block by block according to the color scheme."""
        snake_index = 0

        # Draw the head
        if self.color_scheme.head_color is not None:
            self.draw_snake_position(self.brain.snake.get_head_position(), self.color_scheme.head_color)
            snake_index += 1

        pattern_index = 0
        pattern = self.color_scheme.body_pattern
        pattern_length = len(pattern)

        pattern_end = self.brain.snake.length() \
            if self.color_scheme.tail_color is None \
            else self.brain.snake.length() - 1

        if self.color_scheme.color_mode == ColorMode.PATTERN_ONCE:
            segment_lengths = [self.brain.snake.length() // pattern_length] * pattern_length
            extra_segment = self.brain.snake.length() % pattern_length

            for i in range(extra_segment):
                segment_lengths[i] += 1

            for pos in self.brain.snake.body_positions[snake_index:pattern_end]:
                if segment_lengths[pattern_index] > 0:
                    self.draw_snake_position(pos, pattern[pattern_index])
                    segment_lengths[pattern_index] -= 1
                    if segment_lengths[pattern_index] <= 0:
                        pattern_index += 1

        else:
            for pos in self.brain.snake.body_positions[snake_index:pattern_end]:
                self.draw_snake_position(pos, self.color_scheme.body_pattern[pattern_index])
                pattern_index = (pattern_index + 1) % len(self.color_scheme.body_pattern)

        if self.color_scheme.tail_color is not None:
            self.draw_snake_position(self.brain.snake.get_tail_position(), self.color_scheme.tail_color)

    def draw_food(self) -> None:
        """Draw the food block using the food color of the color scheme."""
        food_x, food_y = self.brain.food.x_coordinate, self.brain.food.y_coordinate
        food_color = self.color_scheme.food_color if self.brain.food.lifetime is None \
            else self.get_special_food_color(self.brain.food.lifetime)
        self.draw_rectangle([food_x, food_y, 1, 1], food_color)

    def display_score(self, score_type: ScoreType = ScoreType.CURRENT,
                      x: int = 0, y: int = 0,
                      score_tag_text: str = "", color=colors.BLACK) -> None:
        """
        Display the requested score (current or high score) at the given coordinates with the tag text in front.

        :param score_type: Score type to define which score to use with the text (current or high).
        :param x: X-coordinate of the text.
        :param y: Y-coordinate of the text.
        :param score_tag_text: Text to write in front of the score, to identify which score it is (e.g. Highscore: 21).
        :param color: Color of the text.
        """
        score = self.brain.high_score if score_type is ScoreType.HIGH else self.brain.current_score
        self.display_text(score_tag_text + str(score), self.score_font, color, x, y)

    def display_scheme_name(self) -> None:
        """Display the name of the color scheme at the top of the screen."""
        self.display_text(self.color_scheme.scheme_name,
                          self.score_font,
                          self.color_scheme.text_color,
                          self.display_width / 2.5, 0)

    def display_game_status(self, color=colors.WHITE) -> None:
        """Display the game status (Paused/Lost/Won) when the game is not currently active."""
        if self.brain.game_paused:
            status_text = {
                GameStatus.ONGOING: "Game Paused",
                GameStatus.LOST: "Game Lost",
                GameStatus.WON: "Game Won"
            }.get(self.brain.game_status, "")

            self.display_text(status_text, self.game_font, color, self.display_width / 2.5, self.display_height / 3)

    def display_instructions(self, color=colors.WHITE) -> None:
        """Display the instructions of the game, depending on the state and what actions are allowed."""
        instructions = [
            "← ↕ → - Move the Snake",
            "Esc  -  Pause the Game",
            "Enter/Space - Continue",
            "S  -  Start a new Game",
            "Q      -     Quit Game"
        ]

        # Continue instruction is left out when the game is over (can't unpause a game that has ended).
        if not self.brain.game_in_play():
            instructions = instructions[0:2] + instructions[3:]

        line_height = self.display_height / 3 * 2
        for line in instructions:
            self.display_text(line, self.instructions_font, color, self.display_width / 2.75, line_height)
            line_height += 30

    # ----------------------------------- COLOR SCHEME METHODS ----------------------------------

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        """
        Set the color scheme of the UI to the custom color_scheme.

        :param color_scheme: Custom color scheme
        """
        self.color_scheme = color_scheme

    def toggle_color_scheme_repeat(self) -> None:
        """
        Toggle the color scheme of the UI between PATTERN_REPEAT and PATTERN_ONCE.
        """
        if self.color_scheme.color_mode == ColorMode.PATTERN_REPEAT:
            self.color_scheme.color_mode = ColorMode.PATTERN_ONCE
        elif self.color_scheme.color_mode == ColorMode.PATTERN_ONCE:
            self.color_scheme.color_mode = ColorMode.PATTERN_REPEAT

    def set_default_color_scheme(self) -> None:
        """Set the color scheme to the default colors."""
        self.set_color_scheme(ColorScheme.get_default_color_scheme())

    def set_ekans_color_scheme(self) -> None:
        """Set the color scheme to ekans (Pokémon) theme."""
        self.set_color_scheme(ColorScheme.get_ekans_color_scheme())

    def set_python_color_scheme(self) -> None:
        """Set the color scheme to Python (programming language) logo theme."""
        self.set_color_scheme(ColorScheme.get_python_color_scheme())

    def set_slytherin_color_scheme(self) -> None:
        """Set the color scheme to Slytherin (Harry Potter house) theme colors."""
        self.set_color_scheme(ColorScheme.get_slytherin_color_scheme())

    def set_rainbow_color_scheme(self) -> None:
        """Set the color scheme to Vibrant Rainbow colors."""
        self.set_color_scheme(ColorScheme.get_rainbow_color_scheme())

    def set_pastel_rainbow_color_scheme(self) -> None:
        """Set the color scheme to Pastel Rainbow colors."""
        self.set_color_scheme(ColorScheme.get_pastel_rainbow_color_scheme())

    def set_estonia_color_scheme(self) -> None:
        """Set the color scheme to Estonia flag colors."""
        self.set_color_scheme(ColorScheme.get_estonia_color_scheme())

    # ----------------------------------------- HELPERS -----------------------------------------

    def draw_snake_position(self, position: tuple[int, int], color: tuple[int, int, int]) -> None:
        self.draw_rectangle([position[0], position[1], 1, 1], color)

    def draw_rectangle(self, block_rectangle: list[int, int, int, int], color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.display, color, self.pixel_rectangle(block_rectangle))

    def display_text(self, text: str, font, color, x, y) -> None:
        text = font.render(text, True, color)
        self.display.blit(text, [x, y])

    def blocks_to_pixels(self, blocks: int) -> int:
        """
        Convert the in-game block measurements to pixel measurements for the display.

        [Multiply the number of blocks with the block_size.]

        :param blocks: Coordinate or measurement size in in-game blocks.
        :return: Block measurement converted to pixels.
        """
        return blocks * self.block_size

    def pixel_rectangle(self, block_rectangle: list[int, int, int, int]) -> list[int, int, int, int]:
        """
        Convert the rectangle in-game block measurements list to pixel information.

        :param block_rectangle: Rectangle information [left_x_coordinate, top_y_coordinate, width, height]
                                measured in in-game blocks.
        :return: Rectangle information [left_x_coordinate, top_y_coordinate, width, height] measured in pixels.
        """
        return [self.blocks_to_pixels(value) for value in block_rectangle]

    def get_special_food_color(self, lifetime: int) -> tuple[int, int, int]:
        if lifetime > 40:
            return colors.BRIGHT_MAGENTA
        elif lifetime > 30:
            return colors.MAGENTA
        elif lifetime > 20:
            return colors.MEDIUM_MAGENTA
        elif lifetime > 10:
            return colors.DIM_MAGENTA
        elif lifetime > 5:
            return colors.DARK_MAGENTA
        else:
            return colors.ALMOST_BLACK_MAGENTA
