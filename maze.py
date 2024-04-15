import sys
import time
from base import *
from mazegen import Maze
import os


# Maze cell dimensions
CELL_WIDTH = 30
CELL_HEIGHT = 30



def find_start_goal(maze):
    start = (2*maze.start_x + 1, 2*maze.start_y+ 1)
    goal = (2*maze.end_x+1, 2*maze.end_y+1)
    return start, goal

def draw_maze(screen, maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                # pygame.draw.rect(screen, BLUE, (j*CELL_WIDTH, i*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
                # use the wall.png file
                wall = pygame.image.load(os.path.join('maze', 'wall.png'))
                wall = pygame.transform.scale(wall, (CELL_WIDTH, CELL_HEIGHT))
                screen.blit(wall, (j*CELL_WIDTH, i*CELL_HEIGHT))
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


def maze(screen):
    maze = Maze(10, 10)
    maze.generate()
    start, goal = find_start_goal(maze)
    position = start
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    idx = 0
    maze_hist = maze.history
    start_time = time.time()
    elapsed_time = 0

    running = True
    moving = False

    reached = False

    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN and reached:
                return STATE.MAIN_MENU
                
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    moving = True  
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    moving = False  

        if (idx < len(maze_hist)):
            screen.fill(BLACK)
            draw_maze(screen, maze_hist[idx])
            pygame.display.flip()  
            idx = (idx + 1) 
            clock.tick(60)

        else:
        
            screen.fill(BLACK)
            draw_maze(screen, maze.maze)
            pygame.draw.rect(screen, WHITE, (position[1]*CELL_WIDTH, position[0]*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            
            if moving and not reached:
                new_position = move(position, event.key)
                if (0 <= new_position[0] < len(maze)) and (0 <= new_position[1] < len(maze[0])) and maze[new_position[0]][new_position[1]] != '#':
                    position = new_position
                    if position == goal:
                        elapsed_time = time.time() - start_time

            if position == goal:
                reached = True
                
        
        if reached:
            draw_text(screen, "Congratulations! You reached the goal.", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, "Time taken: {:.2f} seconds".format(elapsed_time), pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            draw_text(screen, "Click anywhere to exit", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        pygame.display.flip()

    return STATE.EXIT