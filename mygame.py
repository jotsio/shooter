import sys, pygame
import pygame.gfxdraw
import random
from levels import *
pygame.init()

#object class
class Object:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.speed = [0.0, 2.0]  
        self.img = pygame.image.load("assets/asteroid.png").convert()
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(x, y)
    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.top > height:
            del self

#Walls class
class Walls:
    def __init__(self, map):
        self.map = map
        self.yOffset = -len(self.map) * gridsize
        self.rect = pygame.Rect(0, self.yOffset, gridsize, gridsize)    
        self.img = pygame.image.load("assets/wall.png").convert()

    def draw(self):
        k = 0
        self.rect[1] += turns * scrollSpeed
        #loop rows
        while k < len(self.map):
            #draw one row of blocks and draw graphics if wall exists
            i = 0
            while i < len(self.map[k]):
                if self.map[k][i] == "#":
                    screen.blit(self.img, self.rect)
                self.rect[0] += gridsize
                i += 1            
            self.rect[0] = 0
            self.rect[1] += gridsize
            k += 1
        self.rect[1] = self.yOffset
    
    def checkCollision(self, rect):
        k = 0
        self.otherRect = rect
        self.rect[1] += turns * scrollSpeed
        #loop rows
        while k < len(self.map):
            #check one row of blocks and mark collision if wall exists
            i = 0
            while i < len(self.map[k]):
                if self.map[k][i] == "#" and self.rect.colliderect(self.otherRect):
                    self.rect[1] = self.yOffset
                    return True
                self.rect[0] += gridsize
                i += 1            
            self.rect[0] = 0
            self.rect[1] += gridsize
            k += 1
        self.rect[1] = self.yOffset
        

#Stars class
class StarField:
    def __init__(self, amount):
        self.n = amount
        self.spd = 0.5
        self.y = [0.0] * amount
        self.x = [0.0] * amount
        self.z = [0.0] * amount
        self.color = [0,0,0] * amount
        self.speed = [0.0] * amount

        #Create star a random.rect and speed
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


#define game

alive = True
size = width, height = 1280, 1080
gridsize = 64
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_RED = 80, 0, 0
bgColor = BLACK
textColor = WHITE
screen = pygame.display.set_mode(size)   
meteorNumber = 0
scrollSpeed = 2
turns = 0
meteorList = []

# Create Stars
stars = StarField(250)

# Create player
player = PlayerShip(width/2,height-100)

# Create level
level1 = Walls(level1_map)

# Create meteors
i = 0
while i < meteorNumber:
    meteorList.append( Object(random.randrange(64, width-64), 0))
    i += 1

# Create text
font = pygame.font.Font('freesansbold.ttf', 48) 
text = font.render('Kuolit!', True, textColor)
textRect = text.get_rect()  
textRect.center = (width // 2, height // 2)  

# Main loop

clock = pygame.time.Clock()

while clock.tick(120) and alive == True:
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

    # Player collision to walls
    if level1.checkCollision(player.rect):
        alive = False
        bgColor = DARK_RED

    # Background update
    screen.fill(bgColor)
    stars.draw()
    level1.draw()

    
    # Player movement and draw
    player.move()
    screen.blit(player.img, player.rect)

    # Enemy movement and draw
    for obj in meteorList:
        screen.blit(obj.img, obj.rect)
        obj.move()

    if alive == False:
        screen.blit(text, textRect)

    pygame.display.flip()
    bgColor = BLACK
    turns += 1

