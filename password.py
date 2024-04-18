from base import *
import string
import sys
import random
import pygame_textinput


# def generate_captcha(length=6):
#     characters = string.ascii_letters + string.digits
#     captcha = ''.join(random.choice(characters) for _ in range(length))
#     return captcha

# def has_captcha(captcha):
#     def check(s):
#         return s == captcha
#     return check

class Captcha:
    def __init__(self, length=6):
        self.characters = string.ascii_letters + string.digits
        self.captcha = ''.join(random.choice(self.characters) for _ in range(length))
        self.satisfy = False
        self.color = RED

    def check(self, s):
        return s == self.captcha



def has_length(s):
    return len(s) >= 5

def has_num(s):
    return any(c.isdigit() for c in s)

def has_upper(s):
    return any(c.isupper() for c in s)

def has_special(s):
    return any(not c.isalnum() for c in s)

def has_add_25(s):
    tot = 0
    for c in s:
        if(c.isdigit()):
            tot += int(c)
    return tot == 25

def has_month(s):
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    return any(m in s.lower() for m in months)

def has_roman(s):
    romans = ["I", "V", "X", "L", "C", "D", "M"]
    return any(r in s for r in romans)

def has_prime(s):
    primes = ["2", "3", "5", "7"]
    #count total number of prime digits
    count = 0
    for c in s:
        if c in primes:
            count += 1
    return count >= 2

def is_pal(s):
    return s == s[::-1]






class Constraint : 
    def __init__(self, message , check_method):
        self.message = message
        self.check_method = check_method
        self.satisfy = False
        self.color = RED
    
    def check(self, s):
        self.satisfy = self.check_method(s)
        if self.satisfy:
            self.color = GREEN
        else:
            self.color = RED

def password(screen, background, arcade = False):
    
    if arcade:
        level = draw_level(screen, background)
    else:
        level = 1
    
    # textinput = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(*OPTION_FONT), font_color=BLACK)
    # textinput.cursor_color = BLACK
    clock = pygame.time.Clock()
    if level == 1:
        c = [None] * 7
        c[0] = Constraint("1). Your password must have atleat 5 characters", has_length)
        c[1] = Constraint("2). Your password must have atleat 1 number", has_num)
        c[2] = Constraint("3). Your password must have atleat 1 uppercase letter", has_upper)
        c[3] = Constraint("4). Your password must have atleat 1 special character", has_special)
        c[4] = Constraint("5). The sum of the digits in your password must be 25", has_add_25)
        c[5] = Constraint("6). Your password must have a month", has_month)
        c[6] = Constraint("7). Your password must have a roman numeral", has_roman)
    else:
        c = [None] * 5
        c[0] = Constraint("1). Your password must have atleat 7 characters", has_length)
        c[1] = Constraint("2). Your password must have atleat 2 prime digits", has_prime)
        c[2] = Constraint("3). Your password must read the same forward & backward", is_pal)
        c[3] = Constraint("4). The sum of the digits in your password must be 25", has_add_25)
        captcha = Captcha()
        c[4] = Constraint(f"5). Your password must have the following captcha {captcha.captcha}", captcha.check)


        
    running = True
    vaild = False
    password_box = pygame.Rect(150, 110, 600, 50)
    passwd = ""
    cursor = True
    loop = 0
    cursor_pos = 0
    
    while running:
        screen.blit(background, (0, 0))
        draw_nav_bar(screen, "Strong Password")
        pygame.draw.rect(screen, WHITE, password_box, border_radius=10)
        draw_password = passwd if level == 1 else "*" * len(passwd)
        draw_text(screen, draw_password[:cursor_pos] + [" ", "|"][cursor] + draw_password[cursor_pos:], pygame.font.Font(*OPTION_FONT), BLACK, 450, 135)
        draw_text(screen, f"Length: {len(passwd)}", pygame.font.Font(*OPTION_FONT), WHITE, 450, 180)
        message_pos_y = 220
        display_constraints = []
        for constraint in c:
            constraint.check(passwd)
            display_constraints.append(constraint)
            if (not constraint.satisfy):
                vaild = False
                break
        else:
            vaild = True

        display_constraints = display_constraints[::-1]

        if vaild:
            draw_text(screen, "Password is vaild", pygame.font.Font(*OPTION_FONT), GREEN, SCREEN_WIDTH // 2, message_pos_y + 200)
            draw_text(screen, "Click Anywhere to Continue....", pygame.font.Font(*OPTION_FONT), WHITE, SCREEN_WIDTH // 2, message_pos_y + 260)
        else:
            for constraint in display_constraints:
                draw_text(screen, constraint.message, pygame.font.Font(*OPTION_FONT), constraint.color, SCREEN_WIDTH // 2, message_pos_y)
                message_pos_y += 60


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return STATE.EXIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if vaild:
                    return STATE.MAIN_MENU

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
                elif event.key == pygame.K_BACKSPACE:
                    if cursor_pos == 0:
                        continue
                    passwd = passwd[:cursor_pos - 1] + passwd[cursor_pos:]
                    cursor_pos = max(0, cursor_pos - 1)
                elif event.key == pygame.K_LEFT:
                    cursor_pos = max(0, cursor_pos - 1)
                elif event.key == pygame.K_RIGHT:
                    cursor_pos = min(len(passwd), cursor_pos + 1)
                else:
                    if event.unicode in string.ascii_letters + string.digits + string.punctuation:
                        passwd = passwd[:cursor_pos] + event.unicode + passwd[cursor_pos:]
                        cursor_pos += 1
                    
        pygame.display.update()
        
        if loop % 60 == 0:
            cursor = not cursor
        loop += 1
        
        clock.tick(60)