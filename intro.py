from base import *
import sys


def intro(screen, background):
    running = True
    messages = [
        "Welcome to Cyber Adventures!",
        "In this game, you will be presented with a series of challenges.",
        "Each challenge will teach you about Cyber Security.",
    ]
    
    timer = pygame.time.Clock()
    intro_text = ScrollText(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, SCREEN_WIDTH - 100, 50,
                            messages, pygame.font.Font(*OPTION_FONT), WHITE, 3)
    next_button = Button(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Next", intro_text.next)
    prev_button = Button(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 + 200, 200, 50, "Previous", intro_text.prev)
    
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
            elif event.type == pygame.MOUSEMOTION:
                next_button.hover(pygame.mouse.get_pos())
                prev_button.hover(pygame.mouse.get_pos())
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
