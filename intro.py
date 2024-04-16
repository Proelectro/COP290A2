from base import *
import sys


def intro(screen, background):
    running = True
    messages = ["You are cyberlink and have been summoned to protect the kingdom of cyberland", 
                "from the invasion of the virus lord hackhound.",
                "But to be able to defeat him, you have to go on an adventure", 
                "and master the weapons of cyber security to be able to save the kingdom."]
    
    timer = pygame.time.Clock()
    intro_text = ScrollText(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH - 100, 50,
                            messages, pygame.font.Font(*OPTION_FONT), WHITE, 3)
    next_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Next", intro_text.next)
    prev_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Previous", intro_text.prev)
    
    while running:
        screen.blit(background, (0, 0))
        timer.tick(TICK_SPEED)
        
        draw_text(screen, "Introduction", pygame.font.Font(*TITLE_FONT), WHITE,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # ScrollText
        intro_text.increment()
        intro_text.draw(screen)
        
        next_button.draw(screen)
        prev_button.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                try:
                    next_button(pygame.mouse.get_pos())
                except IndexError:
                    return STATE.MAIN_MENU
                
                try:
                    prev_button(pygame.mouse.get_pos())
                except IndexError:
                    pass
    return 0
