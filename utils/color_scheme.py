from enums.color_mode import ColorMode
from utils import colors


class ColorScheme:
    """
    Color Scheme class to display the UI in different color schemes.

    The scheme has:
        * a name, that can be used for display, along with a color that is recommended for the text,
        * color for displaying the food elements,
        * which mode the snake should be styled in (solid color, pattern repeating, pattern once),
        * pattern, which should be represented on the snake,
        * head color, if set the snake's head will be displayed with the color,
        * tail color, if set the snake's tail will be displayed with the color.
    """

    def __init__(self, scheme_name: str,
                 color_mode: ColorMode,
                 food_color: tuple[int, int, int],
                 pattern: list[tuple[int, int, int]],
                 head_color: tuple[int, int, int] = None,
                 tail_color: tuple[int, int, int] = None,
                 text_color: tuple[int, int, int] = None):
        """
        Color Scheme constructor method.

        :param scheme_name: Name of the color scheme.
        :param color_mode: Color mode for the snake pattern.
        :param food_color: Color of the food. (This color does not extend to super foods.)
        :param pattern: Pattern of the snake's body.
                        If the color mode is set to PATTERN_ONCE, the body pattern is displayed once
                        across the snake's body.
                        The length of each pattern color depends on the length of the snake.
                        The segments get longer starting from the head.
                        If the color mode is set to PATTERN_REPEAT, the body pattern is displayed repeatedly
                        until the end of the snake.
        :param head_color: The color to use for the snake's head.
                           If the head color is set, then the body pattern will start after the head.
        :param tail_color: The color to use for the snake's tail.
                           If the tail color is set, then the body pattern will end before the tail.
        :param text_color: Recommended color to display text in, that matches the color scheme.
        """
        self.scheme_name = scheme_name

        self.color_mode = color_mode

        self.head_color = head_color
        self.tail_color = tail_color

        self.food_color = food_color

        self.body_pattern = pattern

        self.text_color = text_color if text_color is not None else colors.BLACK

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
                           [colors.GREEN],
                           None,
                           None,
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
                           ColorMode.SOLID,
                           colors.EKANS_GREEN,
                           [colors.EKANS_PURPLE],
                           None,
                           colors.EKANS_YELLOW,
                           colors.EKANS_PURPLE)

    @staticmethod
    def get_python_color_scheme():
        """
        Python color scheme is inspired by the programming language as the game is written in it,
        and it doubles as a well-known snake species:
         * Snake is striped with blue and yellow (colors of the Python logo),
         * Food is white.

        :return: Color Scheme object with the Python color scheme property values.
        """
        return ColorScheme("Python",
                           ColorMode.PATTERN_REPEAT,
                           colors.PYTHON_WHITE,
                           [colors.PYTHON_BLUE, colors.PYTHON_YELLOW],
                           None,
                           None,
                           colors.PYTHON_BLUE)

    @staticmethod
    def get_slytherin_color_scheme():
        """
        Slytherin color scheme is inspired by the Harry Potter house Slytherin, which has a snake as the mascot:
            * Snake is silver with a green head (Slytherin colors),
            * Food is golden to represent the Golden snitch.

        :return: Color Scheme object with the Slytherin color scheme property values.
        """
        return ColorScheme("Slytherin",
                           ColorMode.SOLID,
                           colors.SLYTHERIN_GOLD,
                           [colors.SLYTHERIN_SILVER],
                           colors.SLYTHERIN_GREEN,
                           None,
                           colors.SLYTHERIN_GREEN)

    @staticmethod
    def get_rainbow_color_scheme():
        """
        Vibrant rainbow color scheme:
            * Snake is a repeating rainbow pattern,
            * Food is white.

        :return: Color Scheme object with the Rainbow color scheme property values.
        """
        return ColorScheme("Rainbow",
                           ColorMode.PATTERN_REPEAT,
                           colors.WHITE,
                           [colors.RAINBOW_RED,
                            colors.RAINBOW_ORANGE,
                            colors.RAINBOW_YELLOW,
                            colors.RAINBOW_GREEN,
                            colors.RAINBOW_BLUE,
                            colors.RAINBOW_INDIGO],
                           None,
                           None,
                           colors.BLACK)

    @staticmethod
    def get_pastel_rainbow_color_scheme():
        """
        Pastel rainbow color scheme:
            * Snake is a repeating rainbow pattern,
            * Food is white.

        :return: Color Scheme object with the Pastel Rainbow color scheme property values.
        """
        return ColorScheme("Pastel",
                           ColorMode.PATTERN_REPEAT,
                           colors.WHITE,
                           [colors.PASTEL_RED,
                            colors.PASTEL_ORANGE,
                            colors.PASTEL_YELLOW,
                            colors.PASTEL_GREEN,
                            colors.PASTEL_BLUE],
                           None,
                           None,
                           colors.BLACK)

    @staticmethod
    def get_estonia_color_scheme():
        """
        Estonia color scheme:
            * Snake is a repeating pattern of the Estonian flag colors,
            * Food is blue.

        :return: Color Scheme object with the Estonia flag colors scheme property values.
        """
        return ColorScheme("Estonia",
                           ColorMode.PATTERN_ONCE,
                           colors.ESTONIA_BLUE,
                           [colors.ESTONIA_BLUE,
                            colors.ESTONIA_BLACK,
                            colors.ESTONIA_WHITE],
                           None,
                           None,
                           colors.BLACK)

    @staticmethod
    def get_windows_color_scheme():
        """
        Windows color scheme:
            * Snake is the colors of the windows logo,
            * Food is white.

        :return: Color Scheme object with the Windows logo colors scheme property values.
        """
        return ColorScheme("Windows",
                           ColorMode.PATTERN_ONCE,
                           colors.WHITE,
                           [colors.WINDOWS_RED,
                            colors.WINDOWS_GREEN,
                            colors.WINDOWS_BLUE,
                            colors.WINDOWS_YELLOW],
                           None,
                           None,
                           colors.BLACK)
