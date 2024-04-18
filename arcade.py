from base import *
import sys

def arcade(screen, background):
    running = True
    
    rocket_button = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2, 250, 60, "Rocket Game")
    # brute_button = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 70 * 1, 250, 60, "Brute Force Game")
    password_button = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 70 * 1, 250, 60, "Password Game")
    maze_button = Button(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 70 * 2, 250, 60, "Maze Game")

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "Arcade", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        rocket_button.draw(screen)
        # brute_button.draw(screen)
        password_button.draw(screen)
        maze_button.draw(screen)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rocket_button(pygame.mouse.get_pos()):
                    return STATE.ROCKET
                # elif brute_forcebutton(pygame.mouse.get_pos()):
                #     return STATE.BRUTEFORCE
                elif password_button(pygame.mouse.get_pos()):
                    return STATE.PASSWORD
                elif maze_button(pygame.mouse.get_pos()):
                    return STATE.MAZE
            elif event.type == pygame.MOUSEMOTION:
                rocket_button.hover(pygame.mouse.get_pos())
                # brute_button.hover(pygame.mouse.get_pos())
                password_button.hover(pygame.mouse.get_pos())
                maze_button.hover(pygame.mouse.get_pos())