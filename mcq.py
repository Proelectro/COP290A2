from base import *
import sys


def mcq(screen, background, question, options, correct_answer, explanation):
    
    running = True
    option_buttons = []
    for i, option in enumerate(options):
        option_buttons.append(Button(SCREEN_WIDTH // 2 - 100, 100 + 60 * i, 200, 50, option))
        option_buttons[-1].color = WHITE
    answered = False
    
    while running:
        
        screen.blit(background, (0, 0))
        
        draw_text(screen, question, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, 50)
        
        for button in option_buttons:
            button.draw(screen)
        
        if answered:
            draw_text(screen, explanation, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, 400)
            draw_text(screen, "Click any where to continue...", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, 450)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if answered:
                    return STATE.MAIN_MENU
                
                for i, button in enumerate(option_buttons):
                    if button(event.pos):
                        answered = True
                        for j, button in enumerate(option_buttons):
                            if j == correct_answer:
                                button.color = GREEN
                            else:
                                button.color = RED
                        break