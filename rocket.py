import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rocket Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
ROCKET_WIDTH = 50
ROCKET_HEIGHT = 50
rocket_img = pygame.image.load('rocket.png')  # Replace 'rocket.png' with your own image file
rocket_img = pygame.transform.scale(rocket_img, (ROCKET_WIDTH, ROCKET_HEIGHT))
rocket_x = SCREEN_WIDTH // 2 - ROCKET_WIDTH // 2
rocket_y = SCREEN_HEIGHT - ROCKET_HEIGHT - 20
rocket_speed = 5

# Bullet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
bullet_img = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
bullet_img.fill(BLUE)
bullet_speed = 10
bullets = []

# Obstacle settings
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
obstacle_img = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_img.fill(RED)
obstacle_speed = 3
obstacles = []

# Game variables
score = 0
clock = pygame.time.Clock()
game_over = False

# Main game loop
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = rocket_x + ROCKET_WIDTH // 2 - BULLET_WIDTH // 2
                bullet_y = rocket_y
                bullets.append(pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT))

    # Move the rocket
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket_x -= rocket_speed
    if keys[pygame.K_RIGHT]:
        rocket_x += rocket_speed

    # Boundary checking for the rocket
    if rocket_x < 0:
        rocket_x = 0
    elif rocket_x > SCREEN_WIDTH - ROCKET_WIDTH:
        rocket_x = SCREEN_WIDTH - ROCKET_WIDTH

    # Move obstacles
    for obstacle in obstacles:
        obstacle.y += obstacle_speed

        # Remove obstacles that go off-screen
        if obstacle.y > SCREEN_HEIGHT:
            obstacles.remove(obstacle)
            score += 1

        # Collision detection with rocket
        if obstacle.colliderect(pygame.Rect(rocket_x, rocket_y, ROCKET_WIDTH, ROCKET_HEIGHT)):
            game_over = True

    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet_speed

        # Remove bullets that go off-screen
        if bullet.y < 0:
            bullets.remove(bullet)

        # Collision detection with obstacles
        for obstacle in obstacles:
            if bullet.colliderect(obstacle):
                obstacles.remove(obstacle)
                bullets.remove(bullet)
                score += 1

    # Create new obstacles
    if random.randint(0, 100) < 3:
        obstacle_x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        obstacle_y = -OBSTACLE_HEIGHT
        obstacles.append(pygame.Rect(obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

    # Clear the screen
    screen.fill(WHITE)

    # Draw the rocket
    screen.blit(rocket_img, (rocket_x, rocket_y))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
font = pygame.font.SysFont(None, 72)
game_over_text = font.render("Game Over", True, (255, 0, 0))
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
score_text = font.render(f"Score: {score}", True, (0, 0, 0))
screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50))
pygame.display.flip()

# Wait for a while before quitting
pygame.time.delay(2000)

# Quit Pygame
pygame.quit()
