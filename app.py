import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 102)

# Game dimensions
WIDTH = 640
HEIGHT = 480
SNAKE_SIZE = 10
SNAKE_SPEED = 15  # Initial speed

# Clock and screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fancy Snake Game')

clock = pygame.time.Clock()

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
apple_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
             random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
apple_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# Function to show the score
def show_score(score):
    value = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])

# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Function to move the snake
def move_snake(direction, snake_pos):
    if direction == 'UP':
        snake_pos[1] -= SNAKE_SIZE
    if direction == 'DOWN':
        snake_pos[1] += SNAKE_SIZE
    if direction == 'LEFT':
        snake_pos[0] -= SNAKE_SIZE
    if direction == 'RIGHT':
        snake_pos[0] += SNAKE_SIZE

# Smarter AI for Snake: Move towards the apple
def get_ai_move(snake_pos, apple_pos):
    if snake_pos[0] < apple_pos[0]:
        return 'RIGHT'
    elif snake_pos[0] > apple_pos[0]:
        return 'LEFT'
    elif snake_pos[1] < apple_pos[1]:
        return 'DOWN'
    elif snake_pos[1] > apple_pos[1]:
        return 'UP'

# Function to create smoother snake movement
def smooth_move(snake_pos, direction):
    if direction == 'UP':
        snake_pos[1] -= SNAKE_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += SNAKE_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= SNAKE_SIZE
    elif direction == 'RIGHT':
        snake_pos[0] += SNAKE_SIZE

# Function to update the snake's position and check collisions
def check_collision(snake_pos, snake_body, apple_pos):
    # Check if snake collides with the boundaries
    if snake_pos[0] >= WIDTH or snake_pos[0] < 0 or snake_pos[1] >= HEIGHT or snake_pos[1] < 0:
        return True
    # Check if snake collides with itself
    for block in snake_body[1:]:
        if block == snake_pos:
            return True
    return False

# Game loop
def game_loop():
    global snake_pos, snake_body, apple_pos, apple_spawn, direction, change_to, score, SNAKE_SPEED

    game_over = False
    game_close = False

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            show_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Capture key events for manual control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Smarter AI Control
        direction = get_ai_move(snake_pos, apple_pos)

        if direction == 'UP' and change_to != 'DOWN':
            change_to = 'UP'
        if direction == 'DOWN' and change_to != 'UP':
            change_to = 'DOWN'
        if direction == 'LEFT' and change_to != 'RIGHT':
            change_to = 'LEFT'
        if direction == 'RIGHT' and change_to != 'LEFT':
            change_to = 'RIGHT'

        # Move snake
        smooth_move(snake_pos, change_to)
        snake_body.insert(0, list(snake_pos))

        # Snake eats apple
        if snake_pos == apple_pos:
            apple_spawn = False
            score += 10
            SNAKE_SPEED += 1  # Increase game speed after eating an apple
        else:
            snake_body.pop()

        # Spawn new apple
        if not apple_spawn:
            apple_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                         random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
        apple_spawn = True

        # Check for collisions
        if check_collision(snake_pos, snake_body, apple_pos):
            game_close = True

        # Refresh the screen
        screen.fill(BLUE)
        for segment in snake_body:
            pygame.draw.rect(screen, GREEN, [segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE])
        pygame.draw.rect(screen, RED, [apple_pos[0], apple_pos[1], SNAKE_SIZE, SNAKE_SIZE])

        show_score(score)
        pygame.display.update()

        # Set the speed of the game
        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

# Run the game
game_loop()
