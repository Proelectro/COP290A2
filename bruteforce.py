from base import *
import sys

BLOCK_SIZE = 100

class Grid:
    
    def __init__(self, grid, center_pos) -> None:
        self.grid = [[[BLUE, RED][x] for x in row] for row in grid]
        self.active = None
        self.center_pos = center_pos
    
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
                dx = clicked_block[0] - self.active[0]
                dy = clicked_block[1] - self.active[1]
                if abs(dx) + abs(dy) == 1:
                    self.swap(self.active, clicked_block)
            self.active = None

def bruteforce(screen, background):
    
    player_grid = Grid([[1, 1, 1], [1, 1, 0], [1, 0, 0]], (0, 0))
    computer_grid = Grid([[1, 1, 1], [1, 1, 0], [1, 0, 0]], (300, 0))
    set_pwd_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, 50, "Set Password")
    running = True
    
    while running:
        screen.blit(background, (0, 0))
        
        player_grid.draw(screen)
        computer_grid.draw(screen)
        set_pwd_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE.EXIT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if set_pwd_button(event.pos):
                    if player_grid == computer_grid:
                        print("Password set successfully!")
                    else:
                        print("Incorrect password!")
                player_grid.on_click(event.pos)
        
        pygame.display.flip()    