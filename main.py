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
from maze import maze

pygame.init()

pygame.mixer.init()
# set 10 chenneles for sound
pygame.mixer.set_num_channels(10)

background_music = pygame.mixer.Sound("sounds/background_music.wav")
background_music.set_volume(0.1)
background_music.play(-1)


# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CyberSavvy Adventures")

# Load background image
background_1 = pygame.transform.scale(pygame.image.load('images/background_hacker.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))  
background_2 = pygame.transform.scale(pygame.image.load('images/white_background.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))



if __name__ == "__main__":
    state = STATE.START_SCREEN
    # state = STATE.PASSWORD
    # state = maze(screen, background_1, False)
    
    while state:
        try:
            if state == STATE.START_SCREEN:
                state = start_screen(screen, background_1)
                
            elif state == STATE.INTRO:
                state = intro(screen, background_1)
            
            elif state == STATE.MAIN_MENU:
                state = main_menu(screen, background_1)
            
            elif state == STATE.ARCADE:
                state = arcade(screen, background_1)
            
            elif state == STATE.ROCKET:
                state = rocket(screen, background_1, True)

            elif state == STATE.BRUTEFORCE:
                state = bruteforce(screen, background_1)            

            elif state == STATE.PASSWORD:
                state = password(screen, background_1, True)
                
            elif state == STATE.MAZE:
                state = maze(screen, background_1, True)
                
            elif state == STATE.STORY:
                try:
                    assert message(screen, background_1, "Story Mode" , ["You will learn about important cyber security concepts in this game."])
                    assert message(screen, background_1,"Passwords", ["Do you know why our passwords should be strong?"])
                    assert bruteforce(screen, background_1)
                    assert message(screen, background_1, "Strong Passwords",
                                ["This was a brute force attack.",
                                    "It is a trial and error method used by hackers to decode encrypted data.", 
                                    "To prevent this, we should use strong passwords.",
                                    "Let us learn how strong passwards can be created."
                                    ])
                    assert password(screen, background_1)
                    
                    assert rocket(screen, background_1)
                
                    assert message(screen, background_1, "Internet Ethics",
                                [
                                    "You have learned about cyber security concepts and internet ethics.",
                                    "Stay safe online.",
                                    
                                    ])   

                    assert message(screen, background_1, "Viruses and Fire Wall",
                                ["Your computer was attacked by many viruses but your firewall has traped them."
                                    ,"Now you need to defeat them to win the game."
                                    ])
                    assert maze(screen, background_1)
                    assert message(screen, background_1, "Congratulations",
                                ["Congratulations! You have won the game."])
                    state = STATE.MAIN_MENU
                except AssertionError:
                    break
                except Escape:
                    state = STATE.MAIN_MENU

            else:
                print("Invalid state", state)
                break
        except Escape:
            state = STATE.MAIN_MENU 
        except AssertionError:
            state = STATE.EXIT    
    pygame.quit()
    sys.exit()