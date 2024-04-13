import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInputVisualizer()

screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
textoutput = pygame.font.Font(None, 36)
feedback = textoutput.render("Hello", True, (0, 0, 0))
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def has_length(s):
    return len(s) > 5

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

num_constraint = 7

c = [None for i in range(num_constraint)]
c[0] = Constraint("your password must have atleat 5 characters", has_length)
c[1] = Constraint("your password must have atleat 1 number", has_num)
c[2] = Constraint("your password must have atleat 1 uppercase letter", has_upper)
c[3] = Constraint("your password must have atleat 1 special character", has_special)
c[4] = Constraint("the sum of the digits in your password must be 25", has_add_25)
c[5] = Constraint("your password must have a month", has_month)
c[6] = Constraint("your password must have a roman numeral", has_roman)


while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    textinput.update(events)
    passwd = textinput.value
    screen.blit(textinput.surface, (10, 10))
    message_pos_x = 10
    message_pos_y = 50
    display_constraints = []
    for constraint in c:
        constraint.check(passwd)
        display_constraints.append(constraint)
        if(not constraint.satisfy):
            break

    display_constraints = display_constraints[::-1]

    for constraint in display_constraints:
        feedback = textoutput.render(constraint.message, True, constraint.color)
        screen.blit(feedback, (message_pos_x, message_pos_y) )
        message_pos_y += 30

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(30)