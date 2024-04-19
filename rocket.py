from base import *
from mcq import mcq
import random


question_1 = "You have a Social Media Account where you share your life updates, You will:"
options_1 = ["Keep it public",
            "Keep it private and accept only known people", 
            "Keep it private and accept everybody",
            ]

answer_1 = 1
explanation_1 = "This is the safest option to keep your personal information private and secure."
question_2 = "You got a popup on a website saving you 100$. All you have to do is to fill out a form. What will you do?"

options_2 = ["Fill the form",
            "Ignore the popup"]
answer_2 = 1
explanation_2 = "It is most probably a scam. You should not give out your information to unknown forms."
            

question_3 = "You get an email to reset the password for your gaming accont."

options_3 = ["Click the link ASAP" , "Delete the email" , "Check the email for any suspicious activity"]
answer_3 = 2

explanation_3 = "This is a common phishing scam. You should always check the email for any suspicious activity before clicking on any links."


question_4 = "You almost got a virus from a website while downloading a pdf"

options_4 = ["Install an antivirus software" , "Install an antivirus and update it regularly" , "Stop using the website"]
answer_4 = 1

explanation_4 = "It isn't just important to have an antivirus software, but also to update it regularly to keep your device secure."

questions = [question_1, question_2, question_3, question_4]
options = [options_1, options_2, options_3, options_4]
answers = [answer_1, answer_2, answer_3, answer_4]
explanations = [explanation_1, explanation_2, explanation_3, explanation_4]

class Player:
    images_off = [pygame.transform.scale(pygame.image.load("images/rocket_up.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_right.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_down.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/rocket_left.png"), (50, 50))]
    images_on = [pygame.transform.scale(pygame.image.load("images/Rocket_up_on.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_right_on.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_down_on.png"), (50, 50)),
                    pygame.transform.scale(pygame.image.load("images/Rocket_left_on.png"), (50, 50))]
    
    
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
        self.vel = 0.8
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

        self.x = max(0, self.x)
        self.x = min(SCREEN_WIDTH - self.width, self.x)
        self.y = max(NAV_BAR_HEIGHT, self.y)
        self.y = min(SCREEN_HEIGHT - self.height, self.y)

class Virus:
    images = [pygame.transform.scale(pygame.image.load('images/virus1.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus2.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus1.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/virus3.png'),(50,50))]

    destroyed_images = [pygame.transform.scale(pygame.image.load('images/deadvirus1.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/deadvirus2.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/deadvirus3.png'),(50,50))
    ,pygame.transform.scale(pygame.image.load('images/deadvirus4.png'),(50,50))]

    
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
        self.dying_period = 150
        self.dying_count = 0
        self.direction = dir
        self.touch = False
        
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
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)
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

    if arcade:
        level = draw_level(screen, background)
    else:
        level = 1
        
    background_music = pygame.mixer.Sound("sounds/background_music.wav")
    background_music.set_volume(0.01)
    
    



    running = True
    
    pygame.mixer.fadeout(True)
    bullet_sfx = pygame.mixer.Sound("sounds/bullet_sfx.wav")
    virus_dying_sfx = pygame.mixer.Sound("sounds/virus_dying_sfx.wav")
    game_over_sfx  = pygame.mixer.Sound("sounds/game_over_sfx.wav")

    pause_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Pause")
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
    score = 0
    mx_score = 0
    bullet = None    
    bullet_active = False
    game_over = False
    viruses = []
    dying_viruses = []
    
    # Initialize background position
    bg_y = 0
    
    pause = False
    # background_music.play()

    while running and not game_over:
        background_music.play()
   
     
        # show the score on top right
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - SCREEN_HEIGHT))
        
        draw_nav_bar(screen, "Rocket")
        pause_button.draw(screen)
        
        if not pause:
            bg_y += 0.05  # Scroll speed
        
        if bg_y >= SCREEN_HEIGHT:
            bg_y = 0
        
        player.draw(screen)
        draw_text(screen, f"Score: {score}", pygame.font.Font(*OPTION_FONT), WHITE, 90, 40)
        
        if bullet_active:
            bullet.draw(screen)
            if not pause:
                bullet.move()
        if not pause:
            if random.randint(0, 1000 * len(viruses) ** 2 // level) == 0:
                dir = random.randint(0, 3)
                virus_vel = 0.15*level
                if dir == 0:
                    viruses.append(Virus(random.randint(0, SCREEN_WIDTH - 50), NAV_BAR_HEIGHT, virus_vel , 0))
                elif dir == 1:
                    viruses.append(Virus(SCREEN_WIDTH, random.randint(NAV_BAR_HEIGHT, SCREEN_HEIGHT - 50), virus_vel, 1))
                elif dir == 2:
                    viruses.append(Virus(random.randint(0, SCREEN_WIDTH - 50), SCREEN_HEIGHT, virus_vel, 2))
                elif dir == 3:
                    viruses.append(Virus(0, random.randint(NAV_BAR_HEIGHT, SCREEN_HEIGHT - 50), virus_vel, 3))

        for virus in viruses:
            virus.draw(screen)
            if not pause:
                virus.move()
                if virus.check_collision_player(player):
                    if arcade:
                        game_over = True
                        break
                    pygame.mixer.Channel(1).play(game_over_sfx)
                    if virus.touch == False:
                        score -= 2
                        score = max(0, score)
                        virus.touch = True
                if bullet_active:
                    if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < NAV_BAR_HEIGHT or bullet.y > SCREEN_HEIGHT:
                        bullet_active = False
                        continue
                    if virus.check_collision_bullet(bullet):
                        pygame.mixer.Channel(2).play(virus_dying_sfx)
                        viruses.remove(virus)
                        virus.alive = False
                        dying_viruses.append(virus)
                        bullet_active = False
                        score += 1
                        if score % 2 == 0 and not arcade and score > mx_score:
                            assert mcq(screen, background, questions[score//2 - 1], options[score // 2 - 1], answers[score // 2 - 1], explanations[score // 2 - 1])
                            if score // 2 == len(questions):
                                return STATE.MAIN_MENU
                        mx_score = max(score, mx_score)
                        continue
            if virus.y > SCREEN_HEIGHT or virus.x < 0 or virus.x > SCREEN_WIDTH or virus.y < NAV_BAR_HEIGHT:
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
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if not bullet_active and not pause:
                    pygame.mixer.Channel(3).play(bullet_sfx)
                    bullet = Bullet(player.x + player.width // 2, player.y + player.height // 2, 1, player.direction)
                    bullet_active = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button(pygame.mouse.get_pos()):
                    pause = not pause
                    if pause:
                        background_music.stop()
                        pause_button.text = "Play"
                    else:
                        background_music.play()
                        pause_button.text = "Pause"

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
                    return STATE.MAIN_MENU
