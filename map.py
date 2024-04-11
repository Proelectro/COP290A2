import pygame as py

py.init()
font = py.font.Font(None, 60)
screen = py.display.set_mode((800, 600))
timer = py.time.Clock()
messages = ["New Game", "Resume", "Quit"]
snip = font.render("", True, 'white')
count = 0
active_message = 0
message = messages[active_message]
speed = 3
done = False
run = True

while run :

    screen.fill((0, 0, 0))
    timer.tick(60)
    py.draw.rect(screen, (255, 255, 255), (300, 200, 200, 50))

    if count < speed * len(message):
        count+=1
    else:
        done = True
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_RETURN and active_message  < len(messages)-1:
                active_message += 1
                done  = False
                message = messages[active_message]
                count = 0
    
    snip = font.render(message[:count//speed], True, 'black')
    screen.blit(snip, (400, 200))
    py.display.flip()