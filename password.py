from base import *
import sys
import pygame_textinput



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

def password(screen, background):
    textinput = pygame_textinput.TextInputVisualizer(font_object=pygame.font.Font(*OPTION_FONT))
    clock = pygame.time.Clock()
    c = [None] * 7
    c[0] = Constraint("1). Your password must have atleat 5 characters", has_length)
    c[1] = Constraint("2). Your password must have atleat 1 number", has_num)
    c[2] = Constraint("3). Your password must have atleat 1 uppercase letter", has_upper)
    c[3] = Constraint("4). Your password must have atleat 1 special character", has_special)
    c[4] = Constraint("5). The sum of the digits in your password must be 25", has_add_25)
    c[5] = Constraint("6). Your password must have a month", has_month)
    c[6] = Constraint("7). Your password must have a roman numeral", has_roman)

    running = True
    vaild = False

    while running:

        screen.blit(background, (0, 0))
        events = pygame.event.get()

        textinput.update(events)
        
        for event in events:
            if event.type == pygame.QUIT:
                return STATE.EXIT

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    raise Escape("Escape")
                if vaild:
                    return STATE.MAIN_MENU

        passwd = textinput.value
        screen.blit(textinput.surface, (200, 50))
        # message_pos_x = 10
        message_pos_y = 100
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
            draw_text(screen, "Password is vaild", pygame.font.Font(*OPTION_FONT), GREEN, SCREEN_WIDTH // 2, message_pos_y)
            draw_text(screen, "Press any key to exit", pygame.font.Font(*OPTION_FONT), BLACK, SCREEN_WIDTH // 2, message_pos_y + 60)
        else:
            for constraint in display_constraints:
                draw_text(screen, constraint.message, pygame.font.Font(*OPTION_FONT), constraint.color, SCREEN_WIDTH // 2, message_pos_y)
                message_pos_y += 60

        
        pygame.display.update()
        clock.tick(30)