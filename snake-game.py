import pygame
import colors
from direction import Direction
from brain import Brain


def display_score(dis, score_font, score, x, score_tag_text=""):
    text = score_font.render(score_tag_text + str(score), True, colors.RED)
    dis.blit(text, [x, 0])


def draw_game_area(dis, borders, base_color=colors.BLACK, border_color=colors.WHITE) -> None:
    dis.fill(base_color)
    for border in borders:
        pygame.draw.rect(dis, border_color, border)


def display_game_status(dis, status_text, display_width, display_height, text_font, color=colors.WHITE):
    text = text_font.render(status_text, True, color)
    dis.blit(text, [display_width / 2, display_height / 3])


def display_instructions(dis, display_width, display_height, text_font, color=colors.WHITE):
    instructions = [
        "Esc - Pause the Game",
        "Enter/Space - Continue",
        "S - Start a new Game",
        "Arrows - Move the Snake",
        "Q - Quit"
    ]
    for line in instructions:
        text = text_font.render(line, True, color)
        dis.blit(text, [display_width / 2.5, display_height / 2])
        display_height += 30


def draw_snake(dis, snake, color=colors.GREEN):
    for pos in snake.positions:
        pygame.draw.rect(dis, color, [pos[0], pos[1], snake.block_size, snake.block_size])


def game_loop():
    game_brain = Brain(800, 600, 10)

    # Game Initialization
    pygame.init()

    # Display Set Up
    dis = pygame.display.set_mode((game_brain.display_width, game_brain.display_height))
    pygame.display.set_caption('Snake (Python) Game')

    # Game Clock Set Up
    clock = pygame.time.Clock()

    # Set up the font
    font_style = pygame.font.SysFont(None, 50)
    score_font = pygame.font.SysFont(None, 25)

    while not game_brain.game_quit:
        # Game is paused
        while game_brain.game_paused:
            draw_game_area(dis, game_brain.get_borders())
            display_instructions(dis, game_brain.display_width, game_brain.display_height, score_font)
            display_score(dis, score_font, game_brain.current_score, 0)

            if not game_brain.game_over:
                display_game_status(dis, "Game Paused!", game_brain.display_width, game_brain.display_height, score_font)
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
            else:
                display_game_status(dis, "Game Over!",
                                    game_brain.display_width, game_brain.display_height, score_font)
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit Game
                            game_brain.quit_game()
                        elif event.key == pygame.K_s:  # New Game
                            game_brain.restart_game()
                        break

            if game_brain.game_quit or game_brain.game_paused:
                continue

        # Game is not Paused
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

        draw_game_area(dis, game_brain.get_borders())
        pygame.draw.rect(dis, colors.RED, [game_brain.food.x_coordinate, game_brain.food.y_coordinate,
                                           game_brain.snake.block_size, game_brain.snake.block_size])
        draw_snake(dis, game_brain.snake)
        display_score(dis, score_font, game_brain.current_score, 0)

        pygame.display.update()

        if game_brain.snake_eating_detection():
            game_brain.snake_eat()
            game_brain.generate_food()

        clock.tick(game_brain.snake.step)

    pygame.quit()
    quit()

game_loop()
