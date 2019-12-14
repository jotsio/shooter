import sys, pygame
import pygame.gfxdraw
import random
pygame.init()

#object class
class Object:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.speed = [0.0, 2.0]  
        self.img = pygame.image.load("assets/asteroid.png")
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(x, y)
    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top > height:
            del self

#Stars class
class StarField:
    def __init__(self, amount):
        self.n = amount
        self.spd = 1.0
        self.y = [0.0] * amount
        self.x = [0.0] * amount
        self.z = [0.0] * amount
        self.color = [0,0,0] * amount
        self.speed = [0.0] * amount

        #Create star a random position and speed
        i = 0
        while i < self.n:
            self.y[i] = random.randrange(0, height)
            self.x[i] = random.randrange(0, width)
            rnd = random.random()
            self.z[i] = rnd * rnd * 255
            c = self.z[i]
            self.color[i] = c, c, c
            self.speed[i] = c / 255.0 * self.spd
            i += 1

    def draw(self): 
        i = 0
        while i < self.n:
            self.y[i] += self.speed[i]
            if self.y[i] > height: self.y[i] = 0
            pygame.gfxdraw.pixel(screen, self.x[i], int(self.y[i]), self.color[i])
            i += 1

#player class
class PlayerShip:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.speed = [0.000, 0.000]  
        self.img = pygame.image.load("assets/ship_default.png")
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(x, y)
        self.maxSpeedX = 4.0
        self.maxSpeedY = 2.0
        self.frictionX = 0.1
        self.frictionY = 0.1
    
    # Passive movement
    def move(self):
        self.rect = self.rect.move(self.speed)
        # Horizontal friction
        if self.speed[0] > 0 :
            self.speed[0] -= self.frictionX
        if self.speed[0] < 0 :
            self.speed[0] += self.frictionX
        # Vertical friction
        if self.speed[1] > 0 :
            self.speed[1] -= self.frictionY
        if self.speed[1] < 0 :
            self.speed[1] += self.frictionY
    
    # Vertical acceleration
    def setSpeedX(self, amount):
        self.speed[0] += amount
        if self.speed[0] > self.maxSpeedX :
            self.speed[0] = self.maxSpeedX
        if self.speed[0] < -self.maxSpeedX :
            self.speed[0] = -self.maxSpeedX

    # Horizontal acceleration
    def setSpeedY(self, amount):
        self.speed[1] += amount
        if self.speed[1] > self.maxSpeedY :
            self.speed[1] = self.maxSpeedY
        if self.speed[1] < -self.maxSpeedY :
            self.speed[1] = -self.maxSpeedY

    def bounceX(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        self.speed[0] = -self.speed[0]
    def bounceY(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        self.speed[1] = -self.speed[1]


#define screen

size = width, height = 1280, 1080
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)   
meteorNumber = 8
meteorList = []

# Create Stars
stars= StarField(800)

# Create player
player = PlayerShip(width/2,height-100)

# Create meteors
i = 0
while i < meteorNumber:
    meteorList.append( Object(random.randrange(64, width-64), 0))
    i += 1

print(meteorList)

clock = pygame.time.Clock()

while clock.tick(120):
    # Keyevents listener
    for event in pygame.event.get():
       if event.type == pygame.QUIT: sys.exit()
    
    pressed = pygame.key.get_pressed()
    player.setSpeedX(pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT])
    player.setSpeedY(pressed[pygame.K_DOWN]-pressed[pygame.K_UP])
    



 

    # bounces from the wall
    if player.rect.left < 0 or player.rect.right > width:
        player.bounceX()
    if player.rect.top < 0 or player.rect.bottom > height:
        player.bounceY()
    
    #background update
    screen.fill(black)
    stars.draw()
    
    # player movement and draw
    player.move()
    screen.blit(player.img, player.rect)

    # enemy movement and draw
    for obj in meteorList:
        screen.blit(obj.img, obj.rect)
        obj.move()

    pygame.display.flip()