from base import *
from itertools import combinations
import sys

BLOCK_SIZE = 100

class Grid:
    
    def __init__(self, grid, center_pos) -> None:
        self.grid = [[[BLUE, RED][x] for x in row] for row in grid]
        self.active = None
        self.center_pos = center_pos
        
    def update(self, grid):
        self.grid = [[[BLUE, RED][x] for x in row] for row in grid]
    
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
        if self.active is None:
            self.active = self.get_block_at(pos)
        else:
            clicked_block = self.get_block_at(pos)
            if clicked_block:
                # dx = clicked_block[0] - self.active[0]
                # dy = clicked_block[1] - self.active[1]
                self.swap(self.active, clicked_block)
            self.active = None

def bruteforce(screen, background):
    
    player_grid = Grid([[1, 0, 0], [0, 1, 1], [1, 1, 0]], (50, 50))
    computer_grid = Grid([[1, 1, 1], [1, 1, 0], [0, 0, 0]], (400, 50))
    set_pwd_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Set Password")
    next_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Next")
    msg1 = "To swap two blocks, click on one block"
    msg2 = "and then click on the other block."
    running = True
    pwd_set = False
    pwd_found = False
    
    perm = combinations([0, 1, 2, 3, 4, 5, 6, 7, 8], 5)
    loop = 0
    
    while running:
        loop += 1
        screen.blit(background, (0, 0))
        
        player_grid.draw(screen)
        computer_grid.draw(screen)
        set_pwd_button.draw(screen)
        draw_text(screen, msg1, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        draw_text(screen, msg2, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        if pwd_found:
            next_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE.EXIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pwd_found and next_button(event.pos):
                        return STATE.MAIN_MENU                
                    
                if not pwd_set:
                    player_grid.on_click(event.pos)
                    if set_pwd_button(event.pos):
                        pwd_set = True
                        msg1 = "Computer is trying to find the password..."
                        msg2 = "By brute force method. Please wait..."

        if pwd_set and not pwd_found and loop % 50 == 0:
            try:
                c = next(perm)
                g = [[(3*i+j in c) for j in range(3)] for i in range(3)]
                computer_grid.update(g)
                if player_grid == computer_grid:
                    pwd_found = True
                    msg1 = "Password found"
                    msg2 = "Well done!"
            except StopIteration:
                pwd_found = True
                msg1 = "Password not found"
                msg2 = "Try again"
            
        
        pygame.display.flip()    