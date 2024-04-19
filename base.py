import pygame
import sys
def split_text(text):
    max_char = 60
    words = text.split()
    lines = [""]
    for word in words:
        if len(lines[-1]) + len(word) + 1 <= max_char:
            lines[-1] += " " + word
        else:
            lines.append(word)
    
    return lines  

# Button class

class Button:
    def __init__(self, x, y, width, height, text, on_click = lambda: None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click
        self.color = WHITE
        self.height = height
        self.width = width
        self.sound = pygame.mixer.Sound("sounds/click.wav")
        self.background_color = GRAY
        self.text_color = BLACK
        # self.inside = False

    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height )
        self.background_rect = pygame.Rect(self.x + 5, self.y + 8, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, self.background_rect, border_radius=(self.height // 4))
        pygame.draw.rect(screen, self.color, self.rect, border_radius=(self.height // 4))
        font = pygame.font.Font(*OPTION_FONT)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def hover(self, pos):
        if self.rect.collidepoint(pos):
            self.color = GRAY
            self.background_color = BLACK
            self.text_color = WHITE
            # if not self.inside:
            #     self.inside = True
            #     self.width += 10
            #     self.height += 10

        else:
            self.color = WHITE
            self.background_color = GRAY
            self.text_color = BLACK
            
            # if self.inside:
            #     self.inside = False
            #     self.width -= 10
            #     self.height -= 10

    def __call__(self, pos):
        if self.rect.collidepoint(pos):
            self.on_click()
            self.sound.play()
            return True
        return False
    


# ScrollText class

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
        text = self.text_list[self.index][:self.scroll_pos_x_speed//self.scroll_speed]
        text_list = split_text(text)
        y = self.y
        for txt in text_list:
            draw_text(screen, txt, self.font, self.color, self.x, y)
            y += self.height
    
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
        


# Draw nav bar
        
def draw_nav_bar(screen, title):
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, NAV_BAR_HEIGHT))
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, NAV_BAR_HEIGHT), 5)
    draw_text(screen, title, pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, NAV_BAR_HEIGHT // 2)

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
    
def draw_level(screen , background, level = True):

    running = True
    es = ["Single Player", "Easy"][level]
    hr = ["Multi Player", "Hard"][level]

    easy = Button(SCREEN_WIDTH // 2 - 200, 200, 400, 50, es)
    hard = Button(SCREEN_WIDTH // 2 - 200, 300, 400, 50, hr)
    while running:
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Level" if level else "Mode")
        easy.draw(screen)
        hard.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy(event.pos):
                    return 1
                if hard(event.pos):
                    return 2
            if event.type == pygame.MOUSEMOTION:
                easy.hover(event.pos)
                hard.hover(event.pos)
        

        


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


# Constants

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
TICK_SPEED = 60
NAV_BAR_HEIGHT = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
DARK_GRAY = (80, 80, 80 )
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 128, 128)
YELLOW = (255, 255, 0)

# Fonts
TITLE_FONT = ("nasalization-rg.otf", 60)
OPTION_FONT = ("nasalization-rg.otf", 25)
