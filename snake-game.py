import pygame
import colors
from direction import Direction
from brain import Brain
from ui import Ui
from score_type import ScoreType


def display_instructions(dis, display_width, display_height, text_font, color=colors.WHITE):
    instructions = [
        "Esc - Pause the Game",
        "Enter/Space - Continue",
        "S - Start a new Game",
        "Arrows - Move the Snake",
        "Q - Quit"
    ]
    display_width = blocks_to_pixels(display_width)
    display_height = blocks_to_pixels(display_height)
    for line in instructions:
        text = text_font.render(line, True, color)
        dis.blit(text, [display_width / 2.5, display_height / 2])
        display_height += 30


def blocks_to_pixels(blocks: int, block_size=10) -> int:
    """
    Converts the in-game block measurements to pixel measurements for the display.
    Multiplies the number of blocks with the block_size.

    :param blocks: Coordinate or measurement size in in-game blocks.
    :param block_size: How many pixels should one blocks be on the screen.
    :return: Block measurement converted to pixels.
    """
    return blocks * block_size


def game_loop():
    game_brain = Brain(80, 60, [2, 2, 2, 2])

    # Game Initialization
    pygame.init()

    ui = Ui(game_brain)
    # Display Set Up
    pygame.display.set_caption('Snake (Python) Game')

    # Game Clock Set Up
    clock = pygame.time.Clock()

    # Set up the font
    font_style = pygame.font.SysFont(None, 50)
    score_font = pygame.font.SysFont(None, 25)

    while not game_brain.game_quit:
        # Game is paused
        while game_brain.game_paused:
            ui.draw_game_area()
            display_instructions(ui.display, game_brain.display_width, game_brain.display_height, score_font)
            ui.display_score(ScoreType.Current)
            ui.display_score(ScoreType.High, ui.display_width * 0.8, 0, "Highscore: ")
            ui.display_game_status()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Continue Game
                        game_brain.unpause_game()
                    elif event.key == pygame.K_q:  # Quit game
                        game_brain.quit_game()
                    elif event.key == pygame.K_s:  # New Game
                        game_brain.restart_game()
                    break

            if game_brain.game_quit or game_brain.game_paused:
                continue

        # Game should not be paused here, but the check is here to ensure it is not paused for the code after
        if game_brain.game_quit or game_brain.game_paused:
            continue

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_brain.pause_game()
                elif event.key == pygame.K_q:
                    game_brain.quit_game()
                elif event.key == pygame.K_LEFT:
                    game_brain.snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    game_brain.snake.change_direction(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    game_brain.snake.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    game_brain.snake.change_direction(Direction.DOWN)

        game_brain.snake.move()

        if game_brain.snake_collision_detection():
            game_brain.game_lost()

        if game_brain.game_quit or game_brain.game_paused:
            continue

        ui.draw_game_area()
        ui.draw_food()
        ui.draw_snake()
        ui.display_score()
        ui.display_score(ScoreType.High, ui.display_width * 0.8, 0, "Highscore: ")

        pygame.display.update()

        if game_brain.snake_eating_detection():
            game_brain.snake_eat()
            game_brain.generate_food()

        clock.tick(game_brain.snake.step * 10)

    pygame.quit()
    quit()


game_loop()
