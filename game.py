import pygame
import time
import random

pygame.init()

crash_sound = pygame.mixer.Sound("crash.wav")

display_width = 1000
display_height = 800

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

ship_width = 73

pause = False

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Space ships')
clock = pygame.time.Clock()

img = pygame.image.load('ship.jpg')
gameIcon = pygame.image.load('icon.png')

pygame.display.set_icon(gameIcon)


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def things(thing_x, thing_y, thing_w, thing_h, color):
    pygame.draw.rect(gameDisplay, color, [thing_x, thing_y, thing_w, thing_h])


def ship(x, y):
    gameDisplay.blit(img, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects(text, large_text)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game_loop()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    largeText = pygame.font.SysFont("comicsansms",90)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quit)

        pygame.display.update()
        clock.tick(15) 


def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w/2), (y + (h/2))))
    gameDisplay.blit(textSurf, textRect)


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def paused():

    pygame.mixer.music.pause()

    largeText = pygame.font.SysFont("comicsansms",90)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quit)

        pygame.display.update()
        clock.tick(15)  


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        largeText = pygame.font.SysFont('comicsansms',100)
        TextSurf, TextRect = text_objects("Space ships", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("START!", 150, 450, 100, 50, green, bright_green, game_loop)
        button('QUIT', 550, 450, 100, 50, red, bright_red, quit)

        pygame.display.update()
        clock.tick(15) 


def game_loop():
    global pause

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_start_x = random.randrange(0, display_width)
    thing_start_y = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        things(thing_start_x, thing_start_y, thing_width, thing_height, black)
        
        thing_start_y += thing_speed
        ship(x, y)
        things_dodged(dodged)

        if x > display_width - ship_width or x < 0:
            crash()

        if thing_start_y > display_height:
            thing_start_y = 0 - thing_height
            thing_start_x = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)


        if y < thing_start_y + thing_height:
            print('y crossover')
            
            if x > thing_start_x and x < thing_start_x + thing_width or x + ship_width > thing_start_x and x + ship_width < thing_start_x + thing_width:
                print('x crossover') 
                crash()
               

        pygame.display.update()
        clock.tick(30)


game_intro()
game_loop()
pygame.quit()
quit()
