from base import *
import random

class Player:
    images_off = [pygame.transform.scale(pygame.image.load("images/rocket_up.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_right.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_down.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_left.png"), (50, 50))]
    images_on = [pygame.transform.scale(pygame.image.load("images/Rocket_up.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_right.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_down.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_left.png"), (50, 50))]
    
    
    def __init__(self, x, y):
        """
        0 : up
        1 : right
        2 : down
        3 : left    
        """

        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = 0.2
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.direction = 0
        self.images = Player.images_off

    def draw(self, screen):
        screen.blit(self.images[self.direction], (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
            self.images = Player.images_on
        else:
            self.images = Player.images_off
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel



        if keys[pygame.K_LEFT]:
            self.direction = 3
        if keys[pygame.K_RIGHT]:
            self.direction = 1
        if keys[pygame.K_UP]:
            self.direction = 0
        if keys[pygame.K_DOWN]:
            self.direction = 2

        # if keys[pygame.K_a]:
        #     self.direction = 3
        # if keys[pygame.K_d]:
        #     self.direction = 1
        # if keys[pygame.K_w]:
        #     self.direction = 0
        # if keys[pygame.K_s]:
        #     self.direction = 2
class Virus:
    images = [pygame.transform.scale(pygame.image.load('images/virus1.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus2.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus1.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus3.png'),(50,50))]

    destroyed_images = [pygame.transform.scale(pygame.image.load('images/rocket_up.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/rocket_right.png'),(50,50))   
    ,pygame.transform.scale(pygame.image.load('images/rocket_down.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/rocket_left.png'),(50,50))]

    
    def __init__(self, x, y, vel, dir=0):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.alive = True
        self.image_index = 0
        self.image_period = 100
        self.count = 0
        self.dying_period = 100
        self.dying_count = 0
        self.direction = dir
        
    def draw(self, screen):
        if self.alive:
            screen.blit(self.images[self.image_index], (self.x, self.y))
            self.hitbox = (self.x, self.y, self.width, self.height)
            self.count  = (self.count + 1) % self.image_period
            if self.count == 0:
                self.image_index = (self.image_index + 1) % len(self.images)

    def draw_destroyed(self, screen):
        if not self.alive and self.dying_count < self.dying_period:
            screen.blit(self.destroyed_images[self.image_index], (self.x, self.y))
            self.count  = (self.count + 1) % self.image_period
            if self.count == 0:
                self.image_index = (self.image_index + 1) % len(self.images)
            self.dying_count  += 1
            
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.direction == 0:
            self.y += self.vel
        elif self.direction == 1:
            self.x -= self.vel
        elif self.direction == 2:
            self.y -= self.vel
        elif self.direction == 3:
            self.x += self.vel

        if self.y > SCREEN_HEIGHT:
            self.alive = False
        if self.x < 0:
            self.alive = False
        if self.x > SCREEN_WIDTH:
            self.alive = False
        if self.y < 0:
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
    
    def __init__(self, x, y, vel, dir):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.vel = vel
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.direction = dir

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        self.hitbox = (self.x, self.y, self.width, self.height)        
    
    def move(self):
        if self.direction == 0:
            self.y -= self.vel
        elif self.direction == 1:
            self.x += self.vel
        elif self.direction == 2:
            self.y += self.vel
        elif self.direction == 3:
            self.x -= self.vel

def rocket(screen, background, arcade = False):      


    background_music = pygame.mixer.Sound("sounds/background_music.wav")
    background_music.set_volume(0.1)
    
    



    running = True
    
    pygame.mixer.fadeout(True)
    bullet_sfx = pygame.mixer.Sound("sounds/bullet_sfx.wav")
    virus_dying_sfx = pygame.mixer.Sound("sounds/virus_dying_sfx.wav")
    game_over_sfx  = pygame.mixer.Sound("sounds/game_over_sfx.wav")


    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    score = 0
    bullet = None    
    bullet_active = False
    game_over = False
    viruses = []
    dying_viruses = []
    
    # Initialize background position
    bg_y = 0
    
    while running and not game_over:
        background_music.play()
      
     
        # show the score on top right
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - SCREEN_HEIGHT))
        
        bg_y += 0.05  # Scroll speed
        
        if bg_y >= SCREEN_HEIGHT:
            bg_y = 0
        
        player.draw(screen)
        draw_text(screen, f"Score: {score}", pygame.font.Font(*OPTION_FONT), WHITE, 60, 20)
        
        if bullet_active:
            bullet.draw(screen)
            bullet.move()
            if bullet.y < 0:
                bullet_active = False
        
        if random.randint(0, 1000 * len(viruses) ** 2) == 0:
            dir = random.randint(0, 3)
            if dir == 0:
                viruses.append(Virus(random.randint(0, SCREEN_WIDTH - 50), 0, 0.15, 0))
            elif dir == 1:
                viruses.append(Virus(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 50), 0.15, 1))
            elif dir == 2:
                viruses.append(Virus(random.randint(0, SCREEN_WIDTH - 50), SCREEN_HEIGHT, 0.15, 2))
            elif dir == 3:
                viruses.append(Virus(0, random.randint(0, SCREEN_HEIGHT - 50), 0.15, 3))

        for virus in viruses:
            virus.draw(screen)
            virus.move()
            if virus.check_collision_player(player):
                game_over = True
                pygame.mixer.Channel(1).play(game_over_sfx)
                break
            if bullet_active:
                if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                    bullet_active = False
                    continue
                if virus.check_collision_bullet(bullet):
                    pygame.mixer.Channel(2).play(virus_dying_sfx)
                    viruses.remove(virus)
                    virus.alive = False
                    dying_viruses.append(virus)
                    bullet_active = False
                    score += 1
                    if score >= 4 and not arcade:
                        return STATE.MAIN_MENU, True
                    continue
            if virus.y > SCREEN_HEIGHT or virus.x < 0 or virus.x > SCREEN_WIDTH or virus.y < 0:
                viruses.remove(virus)
                score -= 1
                score = max(0, score)
        for virus in dying_viruses:
            virus.draw_destroyed(screen)
            if virus.dying_count >= virus.dying_period:
                dying_viruses.remove(virus)
            
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if not bullet_active:
                    pygame.mixer.Channel(3).play(bullet_sfx)
                    bullet = Bullet(player.x + player.width // 2, player.y, 1, player.direction)
                    bullet_active = True
        player.move()
        
    while game_over:
        screen.blit(background, (0, 0))
        draw_text(screen, "Game Over", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        draw_text(screen, f"Your Score Was : {score}", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 )
        draw_text(screen, "Click to return to the main menu", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
                return STATE.EXIT, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    return STATE.MAIN_MENU, False
