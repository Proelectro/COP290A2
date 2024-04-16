from base import *
import sys


def message(screen, background, title, text_list):
    running = True
    
    timer = pygame.time.Clock()
    msg_text = ScrollText(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH - 100, 50,
                            text_list, pygame.font.Font(*OPTION_FONT), WHITE, 3)
    next_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Next", msg_text.next)
    prev_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Previous", msg_text.prev)
    
    while running:
        screen.blit(background, (0, 0))
        timer.tick(TICK_SPEED)
        
        draw_text(screen, title, pygame.font.Font(*TITLE_FONT), WHITE,
                  SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # ScrollText
        msg_text.increment()
        msg_text.draw(screen)
        
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
                except:
                    return STATE.MAIN_MENU
                try:
                    prev_button(pygame.mouse.get_pos())
                except:
                    pass
    return 0
    