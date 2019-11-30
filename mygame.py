import sys, pygame
pygame.init()

size = width, height = 800, 600
speed = [0, 0]
startPos = [400, 500]
black = 0, 0, 0


screen = pygame.display.set_mode(size)

ship = pygame.image.load("assets/ship_default.png")
shipRect = ship.get_rect()
shipRect = shipRect.move(startPos)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
        shipRect = shipRect.move(speed)
        # checks keypresses
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            speed[0] = -2
        if pressed[pygame.K_RIGHT]:
            speed[0] = 2
        # bounces from the wall
        if shipRect.left < 0 or shipRect.right > width:
           speed[0] = -speed[0]
        if shipRect.top < 0 or shipRect.bottom > height:
           speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ship, shipRect)
    pygame.display.flip()