import pygame

class Button:
    def __init__(self, x, y, width, height, text, on_click):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def __call__(self, pos):
        if self.rect.collidepoint(pos):
            self.on_click()
            return True
        return False
    
def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)

# Fonts
TITLE_FONT = (None, 60)
OPTION_FONT = (None, 40)
