import pygame
from enums.direction import Direction
from brain import Brain
from ui import Ui


def game_loop():
    game_brain = Brain(80, 60, [])

    pygame.init()

    ui = Ui(game_brain)
    pygame.display.set_caption('Snake (Python) Game')

    clock = pygame.time.Clock()

    while not game_brain.game_quit:

        while game_brain.game_paused:
            ui.draw_game()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:  # Continue Game
                        game_brain.unpause_game()
                    elif event.key == pygame.K_q:  # Quit game
                        game_brain.quit_game()
                    elif event.key == pygame.K_s:  # New Game
                        game_brain.restart_game()
                    elif event.key == pygame.K_z:
                        ui.set_slytherin_color_scheme()
                    elif event.key == pygame.K_p:
                        ui.set_python_color_scheme()
                    elif event.key == pygame.K_e:
                        ui.set_ekans_color_scheme()
                    elif event.key == pygame.K_DELETE:
                        ui.set_default_color_scheme()
                    break

            if game_brain.game_quit:
                break

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
                elif event.key == pygame.K_z:
                    ui.set_slytherin_color_scheme()
                elif event.key == pygame.K_p:
                    ui.set_python_color_scheme()
                elif event.key == pygame.K_e:
                    ui.set_ekans_color_scheme()
                elif event.key == pygame.K_DELETE:
                    ui.set_default_color_scheme()

        if game_brain.game_quit or game_brain.game_paused:
            continue

        game_brain.snake.move()

        if game_brain.snake_collision_detection():
            game_brain.finish_game()

        ui.draw_game()
        pygame.display.update()

        if game_brain.snake_eating_detection():
            game_brain.snake_eat()
            # Currently the game only ends, if the snake collides with itself or with a border
            # By commenting this in, the game will end the moment the snake reaches its maximum capacity
            # if game_brain.snake_at_max_capacity():
            #     game_brain.finish_game()
            game_brain.generate_food()

        clock.tick(game_brain.snake.step * 10)

    pygame.quit()
    quit()


game_loop()
