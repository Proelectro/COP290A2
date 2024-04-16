import pygame
from pygame.locals import *
 
pygame.init()
 
window = pygame.display.set_mode((600, 600))
 
 
image_sprite = [pygame.image.load("Sprite1.png"),
                pygame.image.load("Sprite2.png"),
                pygame.image.load("Sprite3.png"),
                pygame.image.load("Sprite4.png")]
 
 
clock = pygame.time.Clock()
value = 0
run = True
moving = False
velocity = 12
 
x = 100
y = 150
 
while run:
 
    clock.tick(30)
 
    for event in pygame.event.get():
 
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
 
        if event.type == pygame.KEYUP:
 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                moving = False
                value = 0
 
    key_pressed_is = pygame.key.get_pressed()
 
    if key_pressed_is[K_LEFT]:
        x -= 8
        moving = True
    if key_pressed_is[K_RIGHT]:
        x += 8
        moving = True
 
    if moving:
        value += 1
 
    if value >= len(image_sprite):
        value = 0
 
    image = image_sprite[value]
 
    image = pygame.transform.scale(image, (180, 180))
 
    window.blit(image, (x, y))
 
    pygame.display.update()
 
    window.fill((255, 255, 255))