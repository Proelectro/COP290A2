import pygame
import sys
from base import *
from start_screen import start_screen
from intro import intro
from main_menu import main_menu
from arcade import arcade

pygame.init()


# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CyberSavvy Adventures")

# Load background image
background = pygame.image.load('background.jpg')  # Make sure to provide the path to your background image




if __name__ == "__main__":
    state = 1
    while state:
        if state == 1:
            state = start_screen(screen, background)
        elif state == 2:
            state = intro(screen, background)
        elif state == 3:
            state = main_menu(screen, background)
        elif state == 4:
            state = arcade(screen, background)
            
        else:
            print("Invalid state", state)
            break
                        
    pygame.quit()
    sys.exit()