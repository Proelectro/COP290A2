import pygame_textinput
import pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInputVisualizer()

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()
textoutput = pygame.font.Font(None, 36)
feedback = textoutput.render("Hello", True, (0, 0, 0))


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

def constraint(s):
    constraints = [has_length, has_num, has_upper, has_special, has_add_25, has_month, has_roman]
    messages = [
        "your password must have atleat 5 characters",
        "your password must have atleat 1 number",
        "your password must have atleat 1 uppercase letter",
        "your password must have atleat 1 special character",
        "the sum of the digits in your password must be 25",
        "your password must have a month",
        "your password must have a roman numeral"
    ]

    num_constraints = len(constraints)

    for i in range(num_constraints):
        if not constraints[i](s):
            return messages[i]
    
    return "Your password is strong"

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)
    # Blit its surface onto the screen
    screen.blit(textinput.surface, (10, 10))
    feedback = textoutput.render(constraint(textinput.value), True, (0, 0, 0))
    screen.blit(feedback, (10, 50))

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    pygame.display.update()
    clock.tick(30)