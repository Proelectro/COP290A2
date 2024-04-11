from base import *
import sys


def main_menu(screen, background):
    running = True
    
    def story_mode():
        return

    def arcade_mode():
        return

    story_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Story Mode", story_mode)
    arcade_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Arcade Mode", arcade_mode)

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "Main Menu", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        story_button.draw(screen)
        arcade_button.draw(screen)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if arcade_button(pygame.mouse.get_pos()):
                    return STATE.ARCADE
    
    return 0
