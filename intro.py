from base import *
import sys


def intro(screen, background):
    running = True

    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "Introduction", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 0
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
    return 0
