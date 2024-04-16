import pygame

class Button:
    def __init__(self, x, y, width, height, text, on_click = lambda: None):
        self.rect = pygame.Rect(x, y, width, height )
        self.text = text
        self.on_click = on_click
        self.color = WHITE
        self.height = height
        self.width = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=(self.height // 4))
        font = pygame.font.Font(*OPTION_FONT)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def __call__(self, pos):
        if self.rect.collidepoint(pos):
            self.on_click()
            return True
        return False

class ScrollText:
    def __init__(self, x, y, width, height, text_list, font, color, speed=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_list = text_list
        self.font = font
        self.color = color
        self.scroll_speed = speed
        self.scroll_pos_x_speed = 0
        self.index = 0
    
    def increment(self):
        if self.scroll_pos_x_speed < len(self.text_list[self.index]) * self.scroll_speed:
            self.scroll_pos_x_speed += 1    
    
    def draw(self, screen):
        draw_text(screen, self.text_list[self.index][:self.scroll_pos_x_speed//self.scroll_speed], 
                  self.font, self.color, self.x, self.y)
    
    def next(self):
        self.index += 1
        self.scroll_pos_x_speed = 0
        if self.index >= len(self.text_list):
            self.index = len(self.text_list) - 1
            raise IndexError("End of text list")
            
    def prev(self):
        self.index -= 1
        self.scroll_pos_x_speed = 0
        if self.index < 0:
            self.index = 0
            raise IndexError("Start of text list")

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


class Escape(Exception):
    pass
class STATE:
    EXIT = 0
    START_SCREEN = 1
    INTRO = 2
    MAIN_MENU = 3
    ARCADE = 4
    ROCKET = 5
    BRUTEFORCE = 6
    PASSWORD = 7
    MAZE = 8
    STORY = 9

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550
TICK_SPEED = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
RED = (120, 0, 0)
BLUE = (0, 0, 255)

# Fonts
TITLE_FONT = ("nasalization-rg.otf", 60)
OPTION_FONT = ("nasalization-rg.otf", 17)
