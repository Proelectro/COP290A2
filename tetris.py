import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5, 0],
     [5, 5, 5, 5]],

    [[6, 6],
     [6, 6]],

    [[0, 7, 0],
     [7, 7, 7],
     [0, 7, 0]]
]

# Create window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Fonts
font = pygame.font.Font(None, 36)

def draw_grid(surface, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def new_piece():
    shape = random.choice(SHAPES)
    piece = {
        "shape": shape,
        "x": GRID_WIDTH // 2 - len(shape[0]) // 2,
        "y": 10
    }
    return piece

def draw_piece(surface, piece):
    shape = piece["shape"]
    color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(surface, color, ((piece["x"] + x) * GRID_SIZE, (piece["y"] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def move_piece(piece, dx, dy, grid):
    piece["x"] += dx
    piece["y"] += dy
    if collide(piece, grid):
        piece["x"] -= dx
        piece["y"] -= dy
        return True
    return False

def rotate(piece):
    piece["shape"] = [list(row) for row in zip(*reversed(piece["shape"]))]

def collide(piece, grid):
    shape = piece["shape"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if piece["x"] + x < 0 or piece["x"] + x >= GRID_WIDTH or piece["y"] + y >= GRID_HEIGHT or grid[piece["y"] + y][piece["x"] + x]:
                    return True
    return False

def merge(piece, grid):
    shape = piece["shape"]
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece["y"] + y][piece["x"] + x] = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

def check_lines(grid):
    lines = 0
    for y in range(GRID_HEIGHT):
        if all(grid[y]):
            del grid[y]
            grid.insert(0, [0] * GRID_WIDTH)
            lines += 1
    return lines

def draw_text(surface, text, x, y):
    rendered_text = font.render(text, True, WHITE)
    surface.blit(rendered_text, (x, y))

def main():
    grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    piece = new_piece()
    clock = pygame.time.Clock()
    game_over = False
    score = 0

    while not game_over:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_piece(piece, -1, 0, grid)
                elif event.key == pygame.K_RIGHT:
                    move_piece(piece, 1, 0, grid)
                elif event.key == pygame.K_DOWN:
                    if not move_piece(piece, 0, 1, grid):
                        merge(piece, grid)
                        lines_cleared = check_lines(grid)
                        score += lines_cleared * 100
                        piece = new_piece()
                        if collide(piece, grid):
                            game_over = True
                elif event.key == pygame.K_UP:
                    rotate(piece)

        if not move_piece(piece, 0, 1, grid):
            merge(piece, grid)
            lines_cleared = check_lines(grid)
            score += lines_cleared * 100
            piece = new_piece()
            if collide(piece, grid):
                game_over = True

        draw_grid(screen, grid)
        draw_piece(screen, piece)
        draw_text(screen, f"Score: {score}", 10, 10)

        pygame.display.flip()
        clock.tick(10)

    draw_text(screen, "Game Over", 150, SCREEN_HEIGHT // 2 - 20)
    draw_text(screen, f"Score: {score}", 160, SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
