import sys
import time
from base import *
from mazegen import Maze
import random
import os

CELL_WIDTH = 30
CELL_HEIGHT = 30
MARGIN = 20

def sign(x):
    return -1 if x < 0 else 1

class Base:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.exist = True
        self.pos = (2 * x + 1, 2 * y + 1)
        self.speed = 1
        self.count = 0

    def __eq__(self, __value: object) -> bool:
        return self.pos == __value.pos
    
    def draw(self, screen):
        self.count += 1
        if self.exist:
            pygame.draw.rect(screen, self.color, (MARGIN + self.pos[1] * CELL_WIDTH, MARGIN + self.pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

class Person(Base):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.moving = False

    def move(self, n, m, maze):
        if self.moving and self.count % self.speed == 0:
            new_pos = (self.pos[0] + self.moving[0], self.pos[1] + self.moving[1])
            if 0 <= new_pos[0] < 2 * n + 1 and 0 <= new_pos[1] < 2 * m + 1 and maze[new_pos[0]][new_pos[1]] != '#':
                self.pos = new_pos
                self.x = (self.pos[0] - 1) // 2
                self.y = (self.pos[1] - 1) // 2
    
class Virus(Base):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.prev = (0, 1)
        self.speed = 2
    def get_closest_player(self, players):
        min_dist = float('inf')
        closest = None
        for player in players:
            dist = (self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2
            if dist < min_dist:
                min_dist = dist
                closest = player
        return closest
        
    def move(self, n, m, maze, players):
        moved = False
        closest_player = self.get_closest_player(players)
        x_diff = closest_player.pos[0] - self.pos[0]
        y_diff = closest_player.pos[1] - self.pos[1]
        high = [(-sign(x_diff), 0), (0, -sign(y_diff))]
        low = [(0, sign(y_diff)), (sign(x_diff), 0)]
        if self.count % self.speed == 0:
            flag = False
            while not moved:
                rnd = random.randint(0, 50)
                if flag or  rnd < 45:
                    direction = random.choices(high + low, weights=[30, 30, 1, 1])[0]
                    new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                elif rnd < 48:
                    direction = self.prev
                    flag = True
                    new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                else:
                    self.x = random.randint(0, n - 1)
                    self.y = random.randint(0, m - 1)
                    new_pos = 2 * self.x + 1, 2 * self.y + 1
                    direction = (0, 1)
                    
                if 0 <= new_pos[0] < 2 * n + 1 and 0 <= new_pos[1] < 2 * m + 1 and maze[new_pos[0]][new_pos[1]] != '#':
                    self.pos = new_pos
                    self.x = (self.pos[0] - 1) // 2
                    self.y = (self.pos[1] - 1) // 2
                    moved = True
                    self.prev = direction
            

def find_start_goal(maze):
    start = ( 2*maze.start_x + 1, 2*maze.start_y+ 1)
    goal = (2*maze.end_x+1,  2*maze.end_y+1)
    return start, goal

def draw_maze(screen, maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                wall = pygame.image.load(os.path.join('images', 'wall.png'))
                wall = pygame.transform.scale(wall, (CELL_WIDTH, CELL_HEIGHT))
                screen.blit(wall, (MARGIN + j*CELL_WIDTH, MARGIN + i*CELL_HEIGHT))

def popup(screen, background,  text):
    running = True
    
    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, text, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, "Click anywhere to continue...", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                running = False
    return 1


def maze(screen, popup_background, arcade = False):
    maze = Maze(8, 12)
    maze.generate()
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    idx = 0
    maze_hist = maze.history
    running = True

    moves = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1)
    }
    player = Person(0, 0, RED)
    virus_1 = Virus(random.randint(0, maze.n - 1), random.randint(0, maze.m - 1), GREEN)
    virus_2 = Virus(random.randint(0, maze.n - 1), random.randint(0, maze.m - 1), GREEN)


    while running:
        screen.fill(BLUE)

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    player.moving = moves[event.key]
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    player.moving = False

        if (idx < len(maze_hist)):
            screen.fill(BLACK)
            draw_maze(screen, maze_hist[idx])
            pygame.display.flip()  
            idx = (idx + 1) 
            clock.tick(60)

        else:
        
            screen.fill(BLACK)
            draw_maze(screen, maze.maze)
            player.draw(screen)
            virus_1.draw(screen)
            virus_2.draw(screen)

            player.move(maze.n, maze.m, maze.maze)
            virus_1.move(maze.n, maze.m, maze.maze, [player])
            virus_2.move(maze.n, maze.m, maze.maze, [player])

            if player == virus_1 and virus_1.exist:
                virus_1.exist = False
                if not arcade:
                    assert popup(screen, popup_background, "You have been caught by the virus!")
            if player == virus_2 and virus_2.exist:
                virus_2.exist = False
                if not arcade:
                    assert popup(screen, popup_background, "You have been caught by the virus!")                
        
        pygame.display.flip()

    return STATE.EXIT