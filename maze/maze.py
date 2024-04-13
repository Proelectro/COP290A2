import pygame
import sys
import time
import random
import subprocess
import os
from mazegen import Maze

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



def find_start_goal(maze):
    start = (2*maze.start_y + 1, 2*maze.start_x+ 1)
    goal = (2*maze.end_y+1, 2*maze.end_x+1)
    return start, goal

def draw_maze(screen, maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
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

# def show_maze(maze):
#     pygame.init()
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Maze Game")
#     maze_hist = maze.history
#     clock = pygame.time.Clock()
#     running = True
#     idx = 0
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         screen.fill(BLACK)
#         draw_maze(screen, maze_hist[idx])
#         pygame.display.flip()  
#         idx = (idx + 1) 
#         clock.tick(30)  
#         if idx == len(maze_hist):
#             return



def play_maze():
    maze = Maze(10, 10)
    maze.generate()
    start, goal = find_start_goal(maze)
    position = start

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    idx = 0
    maze_hist = maze.history
    start_time = time.time()
    elapsed_time = 0

    running = True
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

        if (idx < len(maze_hist)):
            screen.fill(BLACK)
            draw_maze(screen, maze_hist[idx])
            pygame.display.flip()  
            idx = (idx + 1) 
            clock.tick(30)

        else:
        
            screen.fill(BLACK)
            draw_maze(screen, maze.maze)
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
    play_maze()
