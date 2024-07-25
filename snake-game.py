import pygame
import colors
from enums.direction import Direction
from brain import Brain
from ui import Ui
from enums.score_type import ScoreType

# add a color option

def game_loop():
    game_brain = Brain(80, 60, [2, 2, 2, 2])

    # Game Initialization
    pygame.init()

    ui = Ui(game_brain)
    # Display Set Up
    pygame.display.set_caption('Snake (Python) Game')

    # Game Clock Set Up
    clock = pygame.time.Clock()

    while not game_brain.game_quit:
        # Game is paused
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
                    break

            if game_brain.game_quit or game_brain.game_paused:
                continue
        # todo fix bug
        # current situation
        # direction is changed
        # the snake does not move forward before the change direction is listened again
        # then when the opposite direction to original is called for
        # self collision is detected, because the direction is not the opposite anymore

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
            game_brain.finish_game()

        if game_brain.game_quit or game_brain.game_paused:
            continue

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
