from base import *
import sys

def arcade(screen, background):
    running = True
    
    def rocket_game():
        return
    
    def virus_game():
        return
    
    rocket_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Rocket Game", rocket_game)
    virus_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Virus Game", virus_game)
    
    while running:
        screen.blit(background, (0, 0))
        
        draw_text(screen, "Arcade", pygame.font.Font(*TITLE_FONT), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        rocket_button.draw(screen)
        virus_button.draw(screen)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 0
            elif event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rocket_button(pygame.mouse.get_pos()):
                    return 5