from base import *
import sys

def arcade(screen, background):
    running = True
    
    rocket_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 80, "Rocket Game")
    brute_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70 * 1, 200, 80, "Brute Force Game")
    password_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70 * 2, 200, 80, "Password Game")
    maze_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70 * 3, 200, 80, "Maze Game")

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "Arcade", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        rocket_button.draw(screen)
        brute_button.draw(screen)
        password_button.draw(screen)
        maze_button.draw(screen)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rocket_button(pygame.mouse.get_pos()):
                    return STATE.ROCKET
                elif brute_button(pygame.mouse.get_pos()):
                    return STATE.BRUTEFORCE
                elif password_button(pygame.mouse.get_pos()):
                    return STATE.PASSWORD
                elif maze_button(pygame.mouse.get_pos()):
                    return STATE.MAZE