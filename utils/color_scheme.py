from enums.color_mode import ColorMode
from utils import colors


class ColorScheme:
    """
    Color Scheme class to display the UI in different color schemes.

    The scheme has:
        * a name, that can be used for display along with a color that is recommended for the text,
        * color for displaying the food elements,
        * which mode the snake should be styled in (solid color, striped, solid color with a different head or tail),
        * colors for styling the snake.
    """

    def __init__(self, scheme_name: str,
                 color_mode: ColorMode,
                 food_color: tuple[int, int, int],
                 main_color: tuple[int, int, int],
                 secondary_color: tuple[int, int, int] = None,
                 text_color: tuple[int, int, int] = None):
        """
        Color Scheme constructor.

        The color scheme has 4 different modes:
            * SOLID,
            * STRIPED,
            * DIFFERENT_HEAD,
            * DIFFERENT_TAIL.

        SOLID mode uses the main_color to color the whole snake,
        from the head to the tail.

        STRIPED mode starts coloring the snake from the head with the main_color and
        then switches between that and secondary_color until the end of the snake.

        DIFFERENT_HEAD mode colors the snake's head with the secondary_color and
        the rest with the main_color.

        DIFFERENT_TAIL mode colors the snake's tail with the secondary_color and
        the rest with the main_color.

        :param scheme_name: Name that can be displayed on the UI, to clarify the scheme's meaning to the user.
        :param color_mode: Color mode to distinguish, how the colors are supposed to be displayed on the snake
                            (SOLID/STRIPED/DIFFERENT_HEAD/DIFFERENT_TAIL).
        :param food_color: Color of the snake's food.
        :param main_color: Main color of the snake's body (for STRIPED the coloring starts from the main_color).
        :param secondary_color: Snake's head's or tail's color or the second stripe's color
        :param text_color: Color that the scheme_name should be displayed in - by default the main snake color.
        """
        self.scheme_name = scheme_name

        self.color_mode = color_mode

        self.head_color = self.body_color = self.secondary_color = self.tail_color = None
        self.food_color = food_color

        self.body_color = main_color

        self.text_color = self.body_color if text_color is None else text_color

        if self.color_mode == ColorMode.STRIPED:
            self.secondary_color = secondary_color
        elif self.color_mode == ColorMode.DIFFERENT_HEAD:
            self.head_color = secondary_color
        elif self.color_mode == ColorMode.DIFFERENT_TAIL:
            self.tail_color = secondary_color

    @staticmethod
    def get_default_color_scheme():
        """
        Default color scheme also known as the classic snake theme:
            * Snake is a solid green color,
            * Food is red.

        :return: Color Scheme object with the default color scheme property values.
        """
        return ColorScheme("Classic",
                           ColorMode.SOLID,
                           colors.RED,
                           colors.GREEN,
                           colors.BLACK)

    @staticmethod
    def get_ekans_color_scheme():
        """
        Ekans color scheme is inspired by the Pokémon snake Ekans (snake backwards):
            * Snake is purple with a yellowish tail (colors of the classic Pokémon),
            * Food is green (color of the shiny - rare - version of the Pokémon).

        :return: Color Scheme object with the ekans color scheme property values.
        """
        return ColorScheme("ekans",
                           ColorMode.DIFFERENT_TAIL,
                           colors.EKANS_GREEN,
                           colors.EKANS_PURPLE,
                           colors.EKANS_YELLOW)

    @staticmethod
    def get_python_color_scheme():
        """
        Python color scheme is inspired by the programming language as the game is written in it, and it doubles as a well-known snake species:
         * Snake is striped with blue and yellow (colors of the Python logo),
         * Food is white.

        :return: Color Scheme object with the Python color scheme property values.
        """
        return ColorScheme("Python",
                           ColorMode.STRIPED,
                           colors.PYTHON_WHITE,
                           colors.PYTHON_BLUE,
                           colors.PYTHON_YELLOW)

    @staticmethod
    def get_slytherin_color_scheme():
        """
        Slytherin color scheme is inspired by the Harry Potter house Slytherin, which has a snake as the mascot:
            * Snake is silver with a green head (Slytherin colors),
            * Food is golden to represent the Golden snitch.

        :return: Color Scheme object with the Slytherin color scheme property values.
        """
        return ColorScheme("Slytherin",
                           ColorMode.DIFFERENT_HEAD,
                           colors.SLYTHERIN_GOLD,
                           colors.SLYTHERIN_SILVER,
                           colors.SLYTHERIN_GREEN,
                           colors.SLYTHERIN_GREEN)
