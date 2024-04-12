import pygame
import sys
import time
import random
import subprocess

def run_cpp_file():
    cpp_file = "mazegen.cpp"  # Replace this with the path to your C++ file
    subprocess.run(["g++", cpp_file])  # Compile the C++ file
    subprocess.run(["./a.out"])  # Run the compiled executable
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display dimensions
WIDTH = 800
HEIGHT = 800

# Maze cell dimensions
CELL_WIDTH = 30
CELL_HEIGHT = 30

def load_maze(filename):
    with open(filename, 'r') as f:
        maze = [list(line.strip()) for line in f]
    return maze

def find_start_goal(maze):
    start = goal = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'G':
                goal = (i, j)
    return start, goal

def draw_maze(screen, maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                pygame.draw.rect(screen, BLUE, (j*CELL_WIDTH, i*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            elif maze[i][j] == 'S':
                pygame.draw.rect(screen, GREEN, (j*CELL_WIDTH, i*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            elif maze[i][j] == 'G':
                pygame.draw.rect(screen, WHITE, (j*CELL_WIDTH, i*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

def move(position, direction):
    moves = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1)
    }
    new_position = (position[0] + moves[direction][0], position[1] + moves[direction][1])
    return new_position

def show_maze(filename , n, m):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    f = open(filename, 'r')
    maze_hist = [list(line.strip()) for line in f]
    num_mazes = len(maze_hist) // (2*n + 1)
    clock = pygame.time.Clock()
    running = True
    idx = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BLACK)
        maze = maze_hist[idx*(2*n + 1):(idx+1)*(2*n + 1)]
        draw_maze(screen, maze)
        pygame.display.flip()  
        idx = (idx + 1) 
        clock.tick(30)  
        if idx == num_mazes:
            return



def play_maze(filename):
    run_cpp_file()
    maze = load_maze(filename)
    start, goal = find_start_goal(maze)
    position = start

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    n = 10
    f = open("mazehist.txt", 'r')
    maze_hist = [list(line.strip()) for line in f]
    num_mazes = len(maze_hist) // (2*n + 1)
    idx = 0

    start_time = time.time()
    elapsed_time = 0

    running = True
    animation = True
    moving = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    moving = True  
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    moving = False  

        if (idx < num_mazes):
            screen.fill(BLACK)
            maze = maze_hist[idx*(2*n + 1):(idx+1)*(2*n + 1)]
            draw_maze(screen, maze)
            pygame.display.flip()  
            idx = (idx + 1) 
            clock.tick(30)

        else:
        
            screen.fill(BLACK)
            draw_maze(screen, maze)
            pygame.draw.rect(screen, WHITE, (position[1]*CELL_WIDTH, position[0]*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            
            if moving:
                new_position = move(position, event.key)
                if (0 <= new_position[0] < len(maze)) and (0 <= new_position[1] < len(maze[0])) and maze[new_position[0]][new_position[1]] != '#':
                    position = new_position
                    if position == goal:
                        elapsed_time = time.time() - start_time

            if position == goal:
                font = pygame.font.SysFont(None, 48)
                text = font.render("Congratulations! You reached the goal.", True, WHITE)
                screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2))
                text = font.render("Time taken: {:.2f} seconds".format(elapsed_time), True, WHITE)
                screen.blit(text, ((WIDTH - text.get_width()) // 2, (HEIGHT - text.get_height()) // 2 + 50))

            pygame.display.flip()
            clock.tick(20)

    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    filename = "maze.txt"  # Change this to your maze file
    play_maze(filename)
