from base import *
from itertools import combinations
import sys

BLOCK_SIZE = 100

def grid_generator():
    zeroes = []
    ones = []
    twoes = []
    for x in list(combinations([0, 1, 2, 3, 4, 5, 6, 7, 8], 5)):
        zeroes = list(x)
        remaining = [i for i in range(9) if i not in zeroes]
        for y in list(combinations(remaining, 3)):
            ones = list(y)
            twoes = list([i for i in remaining if i not in ones])
            grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for on in ones:
                grid[on // 3][on % 3] = 1
            for tw in twoes:
                grid[tw // 3][tw % 3] = 2
            yield grid

class Grid:
    
    def __init__(self, grid, center_pos) -> None:
        self.grid = [[[YELLOW, BLUE, RED ][x] for x in row] for row in grid]
        self.active = None
        self.center_pos = center_pos
        
    def update(self, grid):
        self.grid = [[[YELLOW, BLUE, RED][x] for x in row] for row in grid]
    
    def __eq__(self, value) -> bool:
        return self.grid == value.grid

    def swap(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]
    
    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE + self.center_pos[0], y * BLOCK_SIZE + self.center_pos[1], BLOCK_SIZE, BLOCK_SIZE))
        for y, row in enumerate(self.grid):
            for x, color in enumerate(row):
                pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE + self.center_pos[0], y * BLOCK_SIZE + self.center_pos[1], BLOCK_SIZE, BLOCK_SIZE), 2)
                
    def get_block_at(self, pos):
        x, y = pos
        block_x = (x - self.center_pos[0]) // BLOCK_SIZE
        block_y = (y - self.center_pos[1]) // BLOCK_SIZE
        if 0 <= block_x < len(self.grid[0]) and 0 <= block_y < len(self.grid):
            return (block_x, block_y)
        return None
    
    def on_click(self, pos):
        swaped = False
        if self.active is None:
            self.active = self.get_block_at(pos)
        else:
            clicked_block = self.get_block_at(pos)
            if clicked_block:
                self.swap(self.active, clicked_block)
                swaped = True
            self.active = None
        return swaped
def bruteforce(screen, background):
    
    player_grid = Grid([[1, 0, 0], [0, 0, 1], [1, 2, 0]], (100, 150))
    computer_grid = Grid([[0, 0, 0], [0, 0, 1], [1, 1, 2]], (500, 150))
    computer_grid.grid = [[BLACK] * 3] * 3
    set_pwd_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Set Password")
    next_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Next")
    msg1 = "To swap two blocks, click on one block"
    msg2 = "and then click on the other block."
    running = True
    pwd_set = False
    pwd_found = False
    
    perm = grid_generator()
    loop = 0
    tries = 0
    swaps = 0
    
    while running:
        loop += 1
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Brute Force")
        player_grid.draw(screen)
        computer_grid.draw(screen)
        set_pwd_button.draw(screen)
        draw_text(screen, f"Attempts: {tries}", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH - 120, 40)
        draw_text(screen, f"Swaps: {swaps}", pygame.font.Font(*OPTION_FONT), WHITE, 90, 40)
        draw_text(screen, msg1, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        draw_text(screen, msg2, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        if pwd_found:
            next_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            elif event.type == pygame.MOUSEMOTION:
                if not pwd_set:
                    set_pwd_button.hover(event.pos)
                if pwd_found:
                    next_button.hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pwd_found and next_button(event.pos):
                        return STATE.MAIN_MENU                
                    
                if not pwd_set:
                    swaps += player_grid.on_click(event.pos)
                    if set_pwd_button(event.pos):
                        pwd_set = True
                        msg1 = "Computer is trying to find the password..."
                        msg2 = "By brute force method. Please wait..."

        if pwd_set and not pwd_found and loop % 5 == 0:
            try:
                c = next(perm)
                computer_grid.update(c)
                tries += 1
                if player_grid == computer_grid:
                    pwd_found = True
                    msg1 = "Hacker Has Found the Password"
                    msg2 = f"in {tries} tries"
            except StopIteration:
                pwd_found = True
                msg1 = "Password not found"
                msg2 = "Try again"
            
        
        pygame.display.flip()    