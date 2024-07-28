import pygame
from enums.direction import Direction
from components.brain import Brain
from components.ui import Ui


def game_loop():

    # PyGame initialization
    pygame.init()
    pygame.display.set_caption('Snake (Python) Game')
    clock = pygame.time.Clock()

    # Initialize UI and Game brain
    game_brain = Brain(80, 60, [])
    ui = Ui(game_brain)

    color_scheme_controls = {
        pygame.K_s: ui.set_slytherin_color_scheme,
        pygame.K_p: ui.set_python_color_scheme,
        pygame.K_e: ui.set_ekans_color_scheme,
        pygame.K_r: ui.set_rainbow_color_scheme,
        pygame.K_b: ui.set_pastel_rainbow_color_scheme,
        pygame.K_t: ui.set_estonia_color_scheme,
        pygame.K_w: ui.set_windows_color_scheme,
        pygame.K_DELETE: ui.set_default_color_scheme,
        pygame.K_CAPSLOCK: ui.toggle_color_scheme_repeat,
    }

    game_paused_controls = {
        pygame.K_ESCAPE: game_brain.quit_game,
        pygame.K_SPACE: game_brain.unpause_game,
        pygame.K_RETURN: game_brain.restart_game,
    }

    game_play_controls = {
        pygame.K_ESCAPE: game_brain.pause_game,
        pygame.K_LEFT: lambda: game_brain.snake.change_direction(Direction.LEFT),
        pygame.K_RIGHT: lambda: game_brain.snake.change_direction(Direction.RIGHT),
        pygame.K_UP: lambda: game_brain.snake.change_direction(Direction.UP),
        pygame.K_DOWN: lambda: game_brain.snake.change_direction(Direction.DOWN),
    }

    # Game Loop
    while not game_brain.game_quit:
        ui.draw_game()
        pygame.display.update()

        # Game Controls
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                # Common Game Controls - Available all the time
                if event.key in color_scheme_controls:
                    color_scheme_controls[event.key]()

                # Paused Game Controls
                if game_brain.game_paused:
                    if event.key in game_paused_controls:
                        game_paused_controls[event.key]()

                # Gameplay Controls
                if not game_brain.game_paused:
                    if event.key in game_play_controls:
                        game_play_controls[event.key]()

                break

        if game_brain.game_quit or game_brain.game_paused:
            continue

        # Game Logic

        game_brain.snake_move()

        ui.draw_game()
        pygame.display.update()

        game_brain.snake_move_effects()

        clock.tick(game_brain.snake.step * 10)

    pygame.quit()
    quit()


game_loop()
