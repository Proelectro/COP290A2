from base import *
import random

class Player:
    image = pygame.image.load('images/rocket.png')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = 0.2
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

class Virus:
    image = pygame.image.load('images/virus.jpeg')
    
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.alive = True
        
    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        self.y += self.vel
        if self.y > SCREEN_HEIGHT:
            self.alive = False
            
    def check_collision_player(self, player):
        if self.hitbox[1] + self.hitbox[3] > player.hitbox[1] and self.hitbox[1] < player.hitbox[1] + player.hitbox[3]:
            if self.hitbox[0] + self.hitbox[2] > player.hitbox[0] and self.hitbox[0] < player.hitbox[0] + player.hitbox[2]:
                return True
        return False
    
    def check_collision_bullet(self, bullet):
        if self.hitbox[1] + self.hitbox[3] > bullet.hitbox[1] and self.hitbox[1] < bullet.hitbox[1] + bullet.hitbox[3]:
            if self.hitbox[0] + self.hitbox[2] > bullet.hitbox[0] and self.hitbox[0] < bullet.hitbox[0] + bullet.hitbox[2]:
                return True
        return False
    
class Bullet:
    
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.width, self.height)        
    
    def move(self):
        self.y -= self.vel

def rocket(screen, background):            
    running = True
    
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    score = 0
    bullet = None    
    bullet_active = False
    game_over = False
    viruses = []
    
    # Initialize background position
    bg_y = 0

    while running and not game_over:
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - SCREEN_HEIGHT))
        
        bg_y += 0.01  # Scroll speed
        
        if bg_y >= SCREEN_HEIGHT:
            bg_y = 0
        
        player.draw(screen)
        
        if bullet_active:
            bullet.draw(screen)
            bullet.move()
            if bullet.y < 0:
                bullet_active = False
        
        if random.randint(0, 1000) == 0:
            viruses.append(Virus(random.randint(0, SCREEN_WIDTH - 50), 0, 0.1))
        
        for virus in viruses:
            virus.draw(screen)
            virus.move()
            if virus.check_collision_player(player):
                game_over = True
                break
            if bullet_active:
                if virus.check_collision_bullet(bullet):
                    viruses.remove(virus)
                    bullet_active = False
                    score += 1
                    if score >= 4:
                        return STATE.MAIN_MENU, True
                    continue
            if virus.y > SCREEN_HEIGHT:
                viruses.remove(virus)
                bullet_active = False
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT, False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not bullet_active:
                        bullet = Bullet(player.x + player.width // 2, player.y, 1)
                        bullet_active = True
        player.move()
        
    while game_over:
        screen.blit(background, (0, 0))
        draw_text(screen, "Game Over", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text(screen, "Click to return to the main menu", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
                return STATE.EXIT, False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return STATE.MAIN_MENU, False
