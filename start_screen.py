from base import *
import sys


def start_screen(screen, background):
    running = True
    def play_button_clicked():
        print("Play button clicked")
        return

    play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Play", play_button_clicked)

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "CyberSavvy Adventures", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Play Button

        play_button.draw(screen)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return STATE.EXIT
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button(pygame.mouse.get_pos()):
                    return STATE.INTRO
    
    return 0
