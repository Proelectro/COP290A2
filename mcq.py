from base import *
import sys


def mcq(screen, background, question, options, correct_answer, explanation):
    
    running = True
    option_buttons = []
    for i, option in enumerate(options):
        option_buttons.append(Button(SCREEN_WIDTH // 2 - 200, 250 + 60 * i, 400, 50, option))
        option_buttons[-1].color = WHITE
    answered = False
    
    while running:
        
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Triva Time")
        q_list = split_text(question)
        y = 150
        for txt in q_list:
            draw_text(screen, txt, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, y)
            y += 50

        for button in option_buttons:
            button.draw(screen)
        
        if answered:
            # draw_text(screen, explanation, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, 500)
            e_list = split_text(explanation)
            y = 500
            if len(e_list) == 1:
                y = 550
            for txt in e_list:
                draw_text(screen, txt, pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, y)
                y += 50
            draw_text(screen, "Click any where to continue...", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, 600)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
                
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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("CyberSavvy Adventures")
    background = pygame.transform.scale(pygame.image.load('images/background.jpg'),(SCREEN_WIDTH, SCREEN_HEIGHT))
    question = "What is the capital of India? very long question very long question very long question very long question"
    options = ["New Delhi", "Mumbai", "Kolkata", "Chennai"]
    correct_answer = 0
    explanation = "New Delhi is the capital of India. Big explantion that cause two lines"
    mcq(screen, background, question, options, correct_answer, explanation)