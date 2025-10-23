import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Load car image (replace with your own if you like)
car_width = 50
car_height = 90
player_car = pygame.Surface((car_width, car_height))
player_car.fill(RED)

# Road boundaries
road_x = WIDTH // 3
road_width = WIDTH // 3

# Enemy car
enemy_car = pygame.Surface((car_width, car_height))
enemy_car.fill((0, 255, 0))

# Fonts
font = pygame.font.SysFont(None, 40)

# Game variables
clock = pygame.time.Clock()
player_x = WIDTH // 2 - car_width // 2
player_y = HEIGHT - car_height - 20
speed = 5
enemy_speed = 7
score = 0

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_enemy():
    return random.randint(road_x + 20, road_x + road_width - car_width - 20), -car_height

enemy_x, enemy_y = reset_enemy()

running = True
while running:
    clock.tick(60)
    screen.fill(GRAY)

    # Draw road
    pygame.draw.rect(screen, BLACK, (road_x, 0, road_width, HEIGHT))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > road_x + 10:
        player_x -= speed
    if keys[pygame.K_RIGHT] and player_x < road_x + road_width - car_width - 10:
        player_x += speed

    # Move enemy
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_x, enemy_y = reset_enemy()
        score += 1
        if score % 5 == 0:
            enemy_speed += 1  # Increase difficulty

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, car_width, car_height)
    if player_rect.colliderect(enemy_rect):
        draw_text("GAME OVER!", RED, WIDTH // 2 - 100, HEIGHT // 2 - 20)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    # Draw cars
    screen.blit(player_car, (player_x, player_y))
    screen.blit(enemy_car, (enemy_x, enemy_y))

    # Draw score
    draw_text(f"Score: {score}", WHITE, 10, 10)

    pygame.display.flip()
