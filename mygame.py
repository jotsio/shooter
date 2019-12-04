import sys, pygame
pygame.init()

#object class
class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        print("Object is ready")

#particle class
class Particle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy  
        print("Particle is ready")  

#player class
class PlayerShip:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.speed = [0, 0]  
        self.img = pygame.image.load("assets/ship_default.png")
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(x, y)
        print("Player is ready")  
    def moveX(self):
        self.rect = self.rect.move(self.speed[0], 0 )
    def setSpeed(self, amount):
        self.speed[0] = amount
    def bounceX(self):
        self.speed[0] = -self.speed[0]
    def bounceY(self):
        self.speed[1] = -self.speed[1]
    

#pelaajan luonti
player = PlayerShip(60,70)
print (player.rect)

size = width, height = 800, 600
black = 0, 0, 0

#ruudun maarittely
screen = pygame.display.set_mode(size)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        # checks keypresses
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            player.setSpeed(-4)
        if pressed[pygame.K_RIGHT]:
            player.setSpeed(4)
        # bounces from the wall
        if player.rect.left < 0 or player.rect.right > width:
           player.bounceX()
        if player.rect.top < 0 or player.rect.bottom > height:
           player.bounceY()
        player.moveX()

    screen.fill(black)
    screen.blit(player.img, player.rect)
    pygame.display.flip()