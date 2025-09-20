import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 0)
BLUE = (30, 144, 255)
YELLOW = (255, 255, 0)
PURPLE = (148, 0, 211)

# --- Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsansms', 30)
big_font = pygame.font.SysFont('comicsansms', 60)

# --- Functions ---
def draw_grid():
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y))

def random_food_position():
    x = random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return x, y

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BLACK, (segment[0], segment[1], CELL_SIZE, CELL_SIZE), 1)  # border

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, (food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

def show_score(score):
    text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(text, [10, 10])

def game_over_screen(score):
    screen.fill(BLACK)
    over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(over_text, [SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//3])
    screen.blit(score_text, [SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2])
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# --- Game Variables ---
snake_pos = [100, 100]
snake_body = [[100, 100]]
direction = "RIGHT"
change_to = direction
speed = FPS
score = 0

food_pos = random_food_position()

# --- Main Game Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_w]:
                change_to = "UP"
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                change_to = "DOWN"
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                change_to = "LEFT"
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                change_to = "RIGHT"

    # Prevent snake from moving in the opposite direction
    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    # Move the snake
    if direction == "UP":
        snake_pos[1] -= CELL_SIZE
    if direction == "DOWN":
        snake_pos[1] += CELL_SIZE
    if direction == "LEFT":
        snake_pos[0] -= CELL_SIZE
    if direction == "RIGHT":
        snake_pos[0] += CELL_SIZE

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == list(food_pos):
        score += 10
        food_pos = random_food_position()
        # Increase speed gradually
        if score % 50 == 0:
            speed += 1
    else:
        snake_body.pop()

    # Game Over conditions
    if (snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or
        snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT):
        game_over_screen(score)
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over_screen(score)

    # Draw everything
    screen.fill(BLACK)
    draw_snake(snake_body)
    draw_food(food_pos)
    draw_grid()
    show_score(score)

    pygame.display.update()
    clock.tick(speed)
