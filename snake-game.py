import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
SPEED = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock and fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 40)

# Show score
def show_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Draw snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

# Show message
def show_message(text, color):
    msg = big_font.render(text, True, color)
    text_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(msg, text_rect)

# Main game loop
def game_loop():
    # Initial snake head position
    x = WIDTH // 2
    y = HEIGHT // 2

    # Initial movement (moving right)
    x_change = BLOCK_SIZE
    y_change = 0

    # Snake starts with 3 blocks
    snake_list = [
        [x - 2 * BLOCK_SIZE, y],
        [x - BLOCK_SIZE, y],
        [x, y]
    ]
    snake_length = 3

    # Food position
    food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)

    # Score
    score = 0

    # Game states
    game_over = False
    game_close = False

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            show_message("Game Over! Press C-Play Again or Q-Quit", RED)
            score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 40))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                # Prevent reverse movement
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # New head position
        new_x = snake_list[-1][0] + x_change
        new_y = snake_list[-1][1] + y_change

        # Wall collision
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            game_close = True
            continue

        # New head
        snake_head = [new_x, new_y]

        # Self collision
        if snake_head in snake_list:
            game_close = True
            continue

        # Add new head
        snake_list.append(snake_head)

        # Check food collision
        if new_x == food_x and new_y == food_y:
            score += 1
            snake_length += 1
            food_x = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
            food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        else:
            # Remove tail if food not eaten
            if len(snake_list) > snake_length:
                del snake_list[0]

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
        draw_snake(snake_list)
        show_score(score)
        pygame.display.update()

        clock.tick(SPEED)

    pygame.quit()
    sys.exit()

# Run game
game_loop()