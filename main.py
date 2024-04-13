import pygame
import sys
from base import *
from start_screen import start_screen
from intro import intro
from main_menu import main_menu
from arcade import arcade
from message import message
from rocket import rocket
from bruteforce import bruteforce
from mcq import mcq
from password import password


pygame.init()


# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CyberSavvy Adventures")

# Load background image
background_1 = pygame.image.load('images/background.jpg')  
background_2 = pygame.image.load('images/white_background.jpg')
background_3 = pygame.image.load('images/background.jpg')
background_4 = pygame.image.load('images/background.jpg')




if __name__ == "__main__":
    # state = STATE.START_SCREEN
    state = STATE.ROCKET
    
    while state:
        if state == STATE.START_SCREEN:
            state = start_screen(screen, background_1)
            
        elif state == STATE.INTRO:
            state = intro(screen, background_2)
        
        elif state == STATE.MAIN_MENU:
            state = main_menu(screen, background_3)
        
        elif state == STATE.ARCADE:
            state = arcade(screen, background_4)
        
        elif state == STATE.ROCKET:
            state, win = rocket(screen, background_1)

        elif state == STATE.BRUTEFORCE:
            state = bruteforce(screen, background_1)            

        elif state == STATE.PASSWORD:
            state = password(screen, background_2)
            
        else:
            print("Invalid state", state)
            break
                        
    pygame.quit()
    sys.exit()