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
        Game UI constructor method.

        :param brain: Game brain, which provides the game state, for which the UI is displayed.
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
            self.draw_rectangle(border, border_color)

    def draw_snake(self) -> None:
        """Draw the snake block by block with the appropriate colors."""
        # Draw the head
        if self.color_scheme.head_color is not None:
            self.draw_block_in_position(self.brain.snake.get_head_position(), self.color_scheme.head_color)

        snake_pattern_start = 0 if self.color_scheme.head_color is None else 1
        snake_pattern_end = self.brain.snake.length() \
            if self.color_scheme.tail_color is None \
            else self.brain.snake.length() - 1

        # Draw the pattern on the body
        if self.color_scheme.color_mode == ColorMode.PATTERN_ONCE:
            self.draw_pattern_once_snake(snake_pattern_start, snake_pattern_end)
        else:
            self.draw_default_snake(snake_pattern_start, snake_pattern_end)

        # Draw the tail
        if self.color_scheme.tail_color is not None:
            self.draw_block_in_position(self.brain.snake.get_tail_position(), self.color_scheme.tail_color)

    def draw_food(self) -> None:
        """Draw the food block using the food color of the color scheme."""
        food_color = self.color_scheme.food_color if self.brain.food.lifetime is None \
            else self.get_special_food_color(self.brain.food.lifetime)
        self.draw_block_in_position(self.brain.food.get_position(), food_color)

    def display_score(self, score_type: ScoreType = ScoreType.CURRENT,
                      x: int = 0, y: int = 0,
                      score_tag_text: str = "", color=colors.BLACK) -> None:
        """
        Display the current or high score.

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

    def display_game_status(self, text_color=colors.WHITE) -> None:
        """Display the game status (Paused/Lost/Won) when the game is not currently active."""
        if self.brain.game_paused:
            status_text = {
                GameStatus.ONGOING: "Game Paused",
                GameStatus.LOST: "Game Lost",
                GameStatus.WON: "Game Won"
            }.get(self.brain.game_status, "")

            self.display_text(status_text, self.game_font, text_color, self.display_width / 2.5, self.display_height / 3)

    def display_instructions(self, text_color=colors.WHITE) -> None:
        """Display the instructions of the game, depending on the state and what actions are allowed."""
        instructions = [
            "← ↕ → - Move the Snake",
            "Esc  -  Pause the Game",
            "Esc (x2)  -  Quit Game",
            "Space    -    Continue",
            "Enter    -    New Game",
        ]

        # 'Continue' instruction is left out when the game is over (can't unpause a game that has ended).
        if not self.brain.game_in_play():
            instructions.pop(3)

        line_height = self.display_height / 3 * 2
        for line in instructions:
            self.display_text(line, self.instructions_font, text_color, self.display_width / 2.75, line_height)
            line_height += 30

    # ----------------------------------- COLOR SCHEME METHODS ----------------------------------

    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        """Set the color scheme of the UI to the custom color_scheme."""
        self.color_scheme = color_scheme

    def toggle_color_scheme_repeat(self) -> None:
        """
        Toggle UI color scheme's color mode between PATTERN_REPEAT and PATTERN_ONCE.

        If the color mode is SOLID, the method has no effect.
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

    def set_windows_color_scheme(self) -> None:
        """Set the color scheme to Microsoft Windows logo colors."""
        self.set_color_scheme(ColorScheme.get_windows_color_scheme())

    # ----------------------------------------- HELPERS -----------------------------------------

    def draw_pattern_once_snake(self, snake_pattern_start: int, snake_pattern_end: int) -> None:
        """
        Draw the snake's patterned body in the PATTERN_ONCE.

        The UI color scheme's body pattern is displayed once across the snake's body.
        The length of each pattern color depends on the length of the snake.
        The segments get longer starting from the head.

        :param snake_pattern_start: Index of the snake position, where to start drawing the pattern from.
        :param snake_pattern_end: Index of the snake position, where to stop drawing the pattern.
        """
        pattern_index = 0
        pattern = self.color_scheme.body_pattern
        pattern_length = len(pattern)

        base_segment_length = self.brain.snake.length() // pattern_length
        extra_segments = self.brain.snake.length() % pattern_length

        segment_counter = base_segment_length if extra_segments <= 0 else base_segment_length + 1
        for pos in self.brain.snake.body_positions[snake_pattern_start:snake_pattern_end]:
            self.draw_block_in_position(pos, pattern[pattern_index])
            segment_counter -= 1
            if segment_counter <= 0:
                pattern_index += 1
                extra_segments -= 1  # Remove an extra segment, before re-calculating, in case it was just used up.
                segment_counter = base_segment_length if extra_segments <= 0 else base_segment_length + 1

    def draw_default_snake(self, snake_pattern_start: int, snake_pattern_end: int) -> None:
        """
        Draw the snake's patterned body in the PATTERN_REPEAT and SOLID color mode.

        The UI color scheme's body pattern is repeatedly iterated over until the end of the snake.

        :param snake_pattern_start: Index of the snake position, where to start drawing the pattern from.
        :param snake_pattern_end: Index of the snake position, where to stop drawing the pattern.
        """
        pattern_index = 0
        for pos in self.brain.snake.body_positions[snake_pattern_start:snake_pattern_end]:
            self.draw_block_in_position(pos, self.color_scheme.body_pattern[pattern_index])
            pattern_index = (pattern_index + 1) % len(self.color_scheme.body_pattern)

    def draw_block_in_position(self, position: tuple[int, int], color: tuple[int, int, int]) -> None:
        """
        Display a 1x1 square block at the given position.

        :param position: The top left corner coordinates of the block.
        :param color: Color to display the block.
        """
        self.draw_rectangle([position[0], position[1], 1, 1], color)

    def draw_rectangle(self, block_rectangle: list[int, int, int, int], color: tuple[int, int, int]) -> None:
        """
        Display the in-game block rectangle in pixels.

        Used to display the in-game block elements of the game.

        :param block_rectangle: Rectangle information [width, height, x, y] measured in in-game blocks.
        :param color: Color to display the rectangle.
        """
        pygame.draw.rect(self.display, color, self.pixel_rectangle(block_rectangle))

    def display_text(self, text: str, font, color, x, y) -> None:
        """
        Display the text on the screen, in the given font and color, at the set coordinates.

        :param text: Text to display on the screen.
        :param font: Font to display the text.
        :param color: Color to display the text in.
        :param x: X-coordinate to display the text at.
        :param y: Y-coordinate to display the text at.
        """
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

    @staticmethod
    def get_special_food_color(lifetime: int) -> tuple[int, int, int]:
        """
        Get the color of the superfood based on how much lifetime it has left.

        :param lifetime: The lifetime the food has left.
        :return: Current color of the superfood.
        """
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
