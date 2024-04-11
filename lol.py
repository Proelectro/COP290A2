import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define constants
WIDTH = 300
HEIGHT = 300
BLOCK_SIZE = 100

# Define game grid and winning pattern
grid = [
    [WHITE, RED, GREEN],
    [GREEN, BLUE, RED],
    [RED, GREEN, BLUE]
]

winning_pattern = [
    [WHITE, RED, GREEN],
    [GREEN, BLUE, RED],
    [RED, GREEN, BLUE]
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Lock Puzzle")

def draw_grid():
    for y, row in enumerate(grid):
        for x, color in enumerate(row):
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def get_block_at(pos):
    x, y = pos
    block_x = x // BLOCK_SIZE
    block_y = y // BLOCK_SIZE
    if 0 <= block_x < len(grid[0]) and 0 <= block_y < len(grid):
        return (block_x, block_y)
    return None

def check_win():
    return grid == winning_pattern

# Main game loop
def main():
    selected_block = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if selected_block is None:
                    selected_block = get_block_at(pygame.mouse.get_pos())
                else:
                    clicked_block = get_block_at(pygame.mouse.get_pos())
                    if clicked_block:
                        dx = clicked_block[0] - selected_block[0]
                        dy = clicked_block[1] - selected_block[1]
                        if abs(dx) + abs(dy) == 1:
                            grid[selected_block[1]][selected_block[0]], grid[clicked_block[1]][clicked_block[0]] = grid[clicked_block[1]][clicked_block[0]], grid[selected_block[1]][selected_block[0]]
                            if check_win():
                                print("Congratulations! You've won!")
                        selected_block = None

        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()

if __name__ == "__main__":
    main()
