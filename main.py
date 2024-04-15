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


# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CyberSavvy Adventures")

# Load background image
background_1 = pygame.image.load('images/background.jpg')  
background_2 = pygame.image.load('images/white_background.jpg')
background_3 = pygame.image.load('images/background.jpg')
background_4 = pygame.image.load('images/background.jpg')




if __name__ == "__main__":
    state = STATE.START_SCREEN
    # state = STATE.ROCKET
    
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
            state, win = rocket(screen, background_1, True)

        elif state == STATE.BRUTEFORCE:
            state = bruteforce(screen, background_1)            

        elif state == STATE.PASSWORD:
            state = password(screen, background_2)
            
        elif state == STATE.MAZE:
            state = maze(screen)
            
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
                assert password(screen, background_2)
                assert message(screen, background_1, "Internet Ethics",
                               [
                                   "Congratulations! You have created a strong password.",
                                   "Now lets see some interesting facts about cyber security and internet ethics.",
                               ])
                win = False
                while not win:
                    state, win = rocket(screen, background_1)
                    assert state
                
                assert mcq(screen, background_1,
                           "What is the full form of URL?",
                            ["Uniform Reasearch Locator",
                            "Uniform Resource Link",
                            "Uniform Resource Locator",
                            ],2,"Uniform Resource Locator")
                win = False
                while not win:
                    state, win = rocket(screen, background_1)
                    assert state
                
                assert mcq(screen, background_1,
                           "Your parents use the same password for all their accounts. Is it safe?",
                            ["Yes",
                            "No",
                            ],1,
                            "Each password should be unique and strong to prevent hacking."
                            )
                win = False
                while not win:
                    state, win = rocket(screen, background_1)
                    assert state
                
                assert mcq(screen, background_1,
                           "You got a popup on a website saving you 100$. All you have to do is to fill out a form. What will you do?",
                           ["Fill the form",
                            "Ignore the popup",
                            ],1, "It is a scam to get your personal information."
                            )
            
                assert message(screen, background_1, "Internet Ethics",
                               [
                                "You have learned about cyber security concepts and internet ethics.",
                                "Stay safe online.",
                                
                                ])   

                assert message(screen, background_1, "Viruses and Fire Wall",
                               ["Your computer was attacked by many viruses but your firewall has traped them."
                                ,"Now you need to defeat them to win the game."
                                ])
                assert maze(screen)
                assert message(screen, background_1, "Congratulations",
                               ["Congratulations! You have won the game."])
                state = STATE.MAIN_MENU
            except AssertionError:
                break

        else:
            print("Invalid state", state)
            break
                        
    pygame.quit()
    sys.exit()