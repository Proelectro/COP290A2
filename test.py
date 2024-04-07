import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CyberSavvy Adventures")

# Load background image
background = pygame.image.load('background.jpg')  # Make sure to provide the path to your background image

# Fonts
title_font = pygame.font.Font(None, 60)
option_font = pygame.font.Font(None, 40)

# Main menu options
options = ["New Game", "Resume", "Quit"]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    running = True

    while running:
        screen.blit(background, (0, 0))
        
        draw_text("CyberSavvy Adventures", title_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        for index, option in enumerate(options):
            draw_text(option, option_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 50)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    sys.exit()

# Call the main menu function
main_menu()
