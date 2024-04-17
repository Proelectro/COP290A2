import pygame
import sys

def password_input(screen, font):
    password = ""
    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500  # Cursor blink interval in milliseconds

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return password
                elif event.key == pygame.K_BACKSPACE:
                    password = password[:-1]
                else:
                    password += event.unicode
        
        # Toggle cursor visibility based on timer
        cursor_timer += pygame.time.get_ticks()
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        
        # Display password with cursor
        password_text = password + ('|' if cursor_visible else '')
        text_surface = font.render(password_text, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Password Input")
    font = pygame.font.Font(None, 36)

    password = password_input(screen, font)
    print("Entered password:", password)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
