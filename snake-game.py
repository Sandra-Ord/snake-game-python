import pygame
from enums.direction import Direction
from components.brain import Brain
from components.ui import Ui


def game_loop():
    game_brain = Brain(80, 60, [])

    pygame.init()

    ui = Ui(game_brain)
    pygame.display.set_caption('Snake (Python) Game')

    clock = pygame.time.Clock()

    while not game_brain.game_quit:
        ui.draw_game()
        pygame.display.update()

        # Game Controls
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_z:
                    ui.set_slytherin_color_scheme()
                elif event.key == pygame.K_p:
                    ui.set_python_color_scheme()
                elif event.key == pygame.K_e:
                    ui.set_ekans_color_scheme()
                elif event.key == pygame.K_r:
                    ui.set_rainbow_color_scheme()
                elif event.key == pygame.K_w:
                    ui.set_pastel_rainbow_color_scheme()
                elif event.key == pygame.K_t:
                    ui.set_estonia_color_scheme()
                elif event.key == pygame.K_DELETE:
                    ui.set_default_color_scheme()
                elif event.key == pygame.K_CAPSLOCK:
                    ui.toggle_color_scheme_repeat()

                # Paused Game Controls
                if game_brain.game_paused:
                    if event.key == pygame.K_ESCAPE:
                        game_brain.quit_game()
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Continue Game
                        game_brain.unpause_game()
                    elif event.key == pygame.K_s:
                        game_brain.restart_game()
                    break

                # Gameplay Controls
                if not game_brain.game_paused:
                    if event.key == pygame.K_ESCAPE:
                        game_brain.pause_game()
                    elif event.key == pygame.K_LEFT:
                        game_brain.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        game_brain.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        game_brain.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        game_brain.snake.change_direction(Direction.DOWN)
                    break
                break

        if game_brain.game_quit or game_brain.game_paused:
            continue

        game_brain.snake_move()

        ui.draw_game()
        pygame.display.update()

        game_brain.snake_move_effects()

        clock.tick(game_brain.snake.step * 10)

    pygame.quit()
    quit()


game_loop()
