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
victory_music = pygame.mixer.Sound("sounds/tadaa.wav")



# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cyber Adventures")

# Load background image
# background_1 = pygame.transform.scale(pygame.image.load('images/purple_background.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))  
background_2 = pygame.transform.scale(pygame.image.load('images/rocket_background.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))
background_1 = pygame.transform.scale(pygame.image.load('images/rocket_background.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))



if __name__ == "__main__":
    # state = STATE.START_SCREEN
    # state = STATE.MAZE
    state = maze(screen, background_1, False)
    
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
                state = rocket(screen, background_2, True)

            elif state == STATE.BRUTEFORCE:
                state = bruteforce(screen, background_1)            

            elif state == STATE.PASSWORD:
                state = password(screen, background_1, True)
                
            elif state == STATE.MAZE:
                state = maze(screen, background_1, True)
                
            elif state == STATE.STORY:
                try:
                    assert message(screen, background_1, "Story Mode" , ["You will learn about important cyber security concepts in this game."])
                    assert message(screen, background_1,"Passwords", ["Do you know why our passwords should be strong?"
                                                                      , "Try creating your own password in the following puzzle."
                                                                      #, "A hacker will try to break your password."
                                                                      ])
                    assert bruteforce(screen, background_1)
                    assert message(screen, background_1, "Strong Passwords",
                                ["This was a brute force attack.",
                                    "It is a trial and error method used by hackers to decode encrypted data.", 
                                    "To prevent this, we should use strong passwords.",
                                    "Let us learn how strong passwards can be created."
                                    ])
                    assert password(screen, background_1)

                    assert message(screen, background_1, "Internet Ethics",
                                   [
                                        "Congratulations! You have created a strong password.",
                                        "Now let us move on to the next challenge.",
                                        "Let us now learn about internet ethics.",
                                        "Move using the arrow keys and shoot using the space bar.",
                                        "Prevent the viruses from entering your computer on the other side."
                                   ])
                    
                    assert rocket(screen, background_1)
                
                    assert message(screen, background_1, "Internet Ethics",
                                [
                                    "You have learned about cyber security concepts and internet ethics.",
                                    "Stay safe online.",
                                    
                                    ])   

                    assert message(screen, background_1, "Viruses and Fire Wall",
                                ["Your computer was attacked by many viruses but your firewall has traped them."
                                    ,"Now you need to catch them all."
                                    ])
                    assert maze(screen, background_1)
                    victory_music.play()

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