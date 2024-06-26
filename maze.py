import sys
import time
from base import *
from mazegen import Maze
import random
import os

CELL_WIDTH = 30
CELL_HEIGHT = 30
MARGIN_TOP = 110
MARGIN_LEFT = 45

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
            # pygame.draw.rect(screen, self.color, (MARGIN + self.pos[1] * CELL_WIDTH, MARGIN + self.pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            pygame.draw.rect(screen, self.color, (MARGIN_LEFT + self.pos[1] * CELL_WIDTH, MARGIN_TOP + self.pos[0] * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


class Person(Base):

    images_open = [pygame.transform.scale(pygame.image.load("images/pac2.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac4.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac3.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac1.png") , (CELL_WIDTH, CELL_HEIGHT))]
    
    images_close = [pygame.transform.scale(pygame.image.load("images/pac6.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac8.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac7.png") , (CELL_WIDTH, CELL_HEIGHT)),
                    pygame.transform.scale(pygame.image.load("images/pac5.png") , (CELL_WIDTH, CELL_HEIGHT))]
    
    


    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.moving = False
        self.direction = 0
        self.speed = 10
        self.image_period = 100
        self.image_count = 0

    def draw(self, screen):
        self.count += 1
        self.image_count  = (self.image_count + 1) % self.image_period
        # screen.blit(self.images[self.direction], (self.pos[1]*CELL_WIDTH + MARGIN, self.pos[0]*CELL_HEIGHT + MARGIN))

        if self.image_count < self.image_period // 2:
            screen.blit(self.images_open[self.direction], (MARGIN_LEFT + self.pos[1]*CELL_WIDTH, MARGIN_TOP + self.pos[0]*CELL_HEIGHT))
        else:
            screen.blit(self.images_close[self.direction], (MARGIN_LEFT + self.pos[1]*CELL_WIDTH, MARGIN_TOP + self.pos[0]*CELL_HEIGHT))

    def move(self, n, m, maze):
        if self.moving and self.count % self.speed == 0:
            new_pos = (self.pos[0] + self.moving[0], self.pos[1] + self.moving[1])
            if 0 <= new_pos[0] < 2 * n + 1 and 0 <= new_pos[1] < 2 * m + 1 and maze[new_pos[0]][new_pos[1]] != '#':
                self.pos = new_pos
                self.x = (self.pos[0] - 1) // 2
                self.y = (self.pos[1] - 1) // 2
    
class Virus(Base):

    images = [pygame.transform.scale(pygame.image.load('images/virus1.png'),(CELL_WIDTH,CELL_HEIGHT))
    ,pygame.transform.scale(pygame.image.load('images/virus2.png'),(CELL_WIDTH,CELL_HEIGHT))
    ,pygame.transform.scale(pygame.image.load('images/virus1.png'),(CELL_WIDTH,CELL_HEIGHT))
    ,pygame.transform.scale(pygame.image.load('images/virus3.png'),(CELL_WIDTH,CELL_HEIGHT))]
    

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.prev = (0, 1)
        self.speed = 30
        self.image_index = 0
        self.image_period = 100

    def get_closest_player(self, players):
        min_dist = float('inf')
        closest = None
        for player in players:
            dist = (self.pos[0] - player.pos[0]) ** 2 + (self.pos[1] - player.pos[1]) ** 2
            if dist < min_dist:
                min_dist = dist
                closest = player
        return closest, min_dist
        
    def move(self, n, m, maze, players):
        moved = False
        closest_player, mn_dist = self.get_closest_player(players)
        x_diff = closest_player.pos[0] - self.pos[0]
        y_diff = closest_player.pos[1] - self.pos[1]
        high = [(-sign(x_diff), 0), (0, -sign(y_diff))]
        low = [(0, sign(y_diff)), (sign(x_diff), 0)]
        if mn_dist < 10:
            p = 95
        else:
            p = 30
        if self.count % self.speed == 0:
            flag = False
            while not moved:
                rnd = random.randint(0, 100)
                if flag or  rnd < p:
                    direction = random.choices(high + low, weights=[30, 30, 1, 1])[0]
                    new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                elif rnd < 100:
                    direction = self.prev
                    flag = True
                    new_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
                else:
                    self.x = random.randint(0, n - 1)
                    self.y = random.randint(0, m - 1)
                    new_pos = 2 * self.x + 1, 2 * self.y + 1
                    direction = (0, 1)

                self.direction = list([(0, 1), (1, 0), (0, -1), (-1, 0)]).index(direction)
                    
                if 0 <= new_pos[0] < 2 * n + 1 and 0 <= new_pos[1] < 2 * m + 1 and maze[new_pos[0]][new_pos[1]] != '#':
                    self.pos = new_pos
                    self.x = (self.pos[0] - 1) // 2
                    self.y = (self.pos[1] - 1) // 2
                    moved = True
                    self.prev = direction

    def draw(self, screen):
        if not self.exist:
            return
        self.count += 1
        # screen.blit(self.images[self.image_index], (self.pos[1]*CELL_WIDTH + MARGIN, self.pos[0]*CELL_HEIGHT + MARGIN))
        screen.blit(self.images[self.image_index], (MARGIN_LEFT + self.pos[1]*CELL_WIDTH, MARGIN_TOP + self.pos[0]*CELL_HEIGHT))
        if self.count % self.image_period == 0:
            self.image_index = (self.image_index + 1) % len(self.images)
        


def draw_maze(screen, maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == '#':
                wall = pygame.image.load(os.path.join('images', 'wall.png'))
                wall = pygame.transform.scale(wall, (CELL_WIDTH, CELL_HEIGHT))
                # screen.blit(wall, (MARGIN + j*CELL_WIDTH, MARGIN + i*CELL_HEIGHT))
                screen.blit(wall, (MARGIN_LEFT + j*CELL_WIDTH, MARGIN_TOP + i*CELL_HEIGHT))

def popup(screen, background,  fact):
    running = True
    text_list = split_text(fact)    
    while running:
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Did you know?")
        y_pos = 210
        for text in text_list:
            # white_box = pygame.Rect(150, y_pos - 25, 600, 50)
            # pygame.draw.rect(screen, WHITE, white_box, border_radius=10)
            draw_text(screen, text, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, y_pos)
            y_pos += 80

        draw_text(screen, "Click anywhere to continue...", pygame.font.Font(*OPTION_FONT), GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
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

def display_final_score(screen, background, score_1, score_2 = -1):
    running = True
    while running:
        screen.blit(background, (0, 0))
        if score_2 == -1:
            draw_nav_bar(screen, "Time Taken")
        else:
            draw_nav_bar(screen, "Score")
        if score_2 == -1:
            draw_text(screen, "Captured all viruses in " + str(score_1) + " seconds", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            draw_text(screen, "Player 1: " + str(score_1), pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, "Player 2: " + str(score_2), pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        draw_text(screen, "Click anywhere to continue...", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
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
    return STATE.MAIN_MENU
def maze(screen, background, arcade = False):

    chomp = pygame.mixer.Sound("sounds/pacman_chomp.wav")
    background_music = pygame.mixer.Sound("sounds/background_music.wav")
    background_music.set_volume(0.01)
    
    
    if arcade:
        num_players = draw_level(screen, background, level = False)
    else:
        num_players = 1
    
    facts = ["A firewall is a network security system that monitors and filters incoming and outgoing network traffic based on predetermined security rules.",
               
                "A VPN, or Virtual Private Network, allows you to create a secure connection to another network over the Internet.",

                "A DDoS attack is a malicious attempt to disrupt normal traffic of a targeted server, service or network by overwhelming the target or its surrounding infrastructure with a flood of Internet traffic.",

             "A brute force attack is a trial-and-error method used to obtain information such as a user password or personal identification number (PIN).",
    ] 
    # popup(screen, background, facts[0])
    # popup(screen, background, facts[1])
    # popup(screen, background, facts[2])
    # popup(screen, background, facts[3])

    maze = Maze(8, 13)
    maze.generate()
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    idx = 0
    maze_hist = maze.history
    running = True
    

    moves_1 = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1)
    }
    
    moves_2 = {
        pygame.K_w: (-1, 0),
        pygame.K_s: (1, 0),
        pygame.K_a: (0, -1),
        pygame.K_d: (0, 1)
    }
    
    if num_players == 2:
        player_1 = Person(maze.n - 1, maze.m - 1 , RED)
        player_2 = Person(0, 0, YELLOW)
    else:
        player_1 = Person(0, 0, RED)
        player_2 = None
    score_1 = 0
    score_2 = 0
    
    viruses = []
    for _ in range(4*num_players):
        viruses.append(Virus(random.randint(0, maze.n - 1), random.randint(0, maze.m - 1), GREEN))
    not_started = True
    while running:
        background_music.play()
        # screen.fill(BLUE)
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Maze")
        if num_players == 2:
            draw_text(screen, "Score: " + str(score_1), pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH - 100, 40)
            draw_text(screen, "Score: " + str(score_2), pygame.font.Font(*OPTION_FONT), WHITE, 100, 40)
        else:
            draw_text(screen, "Score: " + str(score_1), pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH - 100, 40)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    player_1.moving = moves_1[event.key]
                    player_1.direction = list(moves_1.keys()).index(event.key)
                    
                if num_players == 2:
                    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                        player_2.moving = moves_2[event.key]
                        player_2.direction = list(moves_2.keys()).index(event.key)
    
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    player_1.moving = False
                    
                if num_players == 2:
                    if event.key in [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                        player_2.moving = False

        if (idx < len(maze_hist)):
            # screen.fill(BLACK)
            draw_maze(screen, maze_hist[idx])
            pygame.display.flip()  
            idx = (idx + 1) 
            clock.tick(100)

        else:
            if not_started:
                start_time = time.time()
                not_started = False
            # screen.fill(BLACK)
            draw_maze(screen, maze.maze)
            player_1.draw(screen)
            if num_players == 2:
                player_2.draw(screen)
            for virus in viruses:
                virus.draw(screen)
            player_1.move(maze.n, maze.m, maze.maze)
            if num_players == 2:
                player_2.move(maze.n, maze.m, maze.maze)
            for i, virus in enumerate(viruses):
                virus.move(maze.n, maze.m, maze.maze, [player_1] + [player_2] * (num_players - 1))
                if player_1 == virus and virus.exist:
                    virus.exist = False
                    score_1 += 1
                    pygame.mixer.Channel(1).play(chomp)
                    if not arcade:
                        assert popup(screen, background, facts[i])
                if num_players == 2 and player_2 == virus and virus.exist:
                    pygame.mixer.Channel(1).play(chomp)
                    virus.exist = False
                    score_2 += 1
                                            
            total_virus = sum([virus.exist for virus in viruses])
            
            if total_virus == 0:
                if num_players == 2:
                    assert display_final_score(screen, background, score_1, score_2)
                else:
                    if arcade:
                        end_time = time.time()
                        time_taken = end_time - start_time
                        ## display only uptill 2 decimal places
                        time_taken = round(time_taken, 2)
                        assert display_final_score(screen, background, time_taken)
                return STATE.MAIN_MENU
        pygame.display.flip()

    return STATE.EXIT