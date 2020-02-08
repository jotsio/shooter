import sys, pygame
import pygame.gfxdraw
import random
import time
from pygame.locals import *
from levels import *


# Global variables
alive = True
size = width, height = 1280, 1080
gridsize = 64
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_RED = 80, 0, 0
bgColor = BLACK
textColor = WHITE

#graphics
GR_MYSHIP = "assets/ship_default.png"





#Walls class
class Walls:
    def __init__(self, map, tiles):
        self.map = map
        self.img = tiles
        self.yOffset = -len(self.map) * gridsize
        self.length = -self.yOffset + height
        self.rect = pygame.Rect(0, self.yOffset, gridsize, gridsize) 

    def draw(self, offset):
        self.offset = offset
        k = 0
        self.rect[1] += self.offset
        #loop rows
        
        while k < len(self.map):
            #draw one row of blocks and draw graphics if wall exists
            i = 0
            
            while i < len(self.map[k]):
                this = self.map[k][i]
                up = "#"
                if k > 0:
                    up = self.map[k-1][i]
                down = "#" 
                if k < len(self.map)-1:
                    down = self.map[k+1][i]
                left = "#"
                if i > 0:
                    left = self.map[k][i-1]
                right = "#"
                if i < len(self.map[k])-1:
                    right = self.map[k][i+1]

                # select which wall asset to use
                if this == "#":
                    if up == "#" and  down == "#" and left == "#" and  right == "#":
                        screen.blit(self.img[0], self.rect)
                    elif up == "." and  down == "." and left == "." and  right == ".":
                        screen.blit(self.img[1], self.rect)
                    elif up == "." and  down == "." and left == "#" and  right == "#":
                        screen.blit(self.img[2], self.rect)
                    elif up == "#" and  down == "#" and left == "." and  right == ".":
                        screen.blit(self.img[3], self.rect)
                    elif up == "." and  down == "#" and left == "." and  right == ".":
                        screen.blit(self.img[4], self.rect)
                    elif up == "#" and  down == "." and left == "." and  right == ".":
                        screen.blit(self.img[5], self.rect)
                    elif up == "." and  down == "." and left == "." and  right == "#":
                        screen.blit(self.img[6], self.rect)
                    elif up == "." and  down == "." and left == "#" and  right == ".":
                        screen.blit(self.img[7], self.rect)
                    elif up == "." and  down == "#" and left == "#" and  right == "#":
                        screen.blit(self.img[8], self.rect)
                    elif up == "#" and  down == "." and left == "#" and  right == "#":
                        screen.blit(self.img[9], self.rect)
                    elif up == "#" and  down == "#" and left == "." and  right == "#":
                       screen.blit(self.img[10], self.rect)
                    elif up == "#" and  down == "#" and left == "#" and  right == ".":
                        screen.blit(self.img[11], self.rect)
                    elif up == "." and  down == "#" and left == "." and  right == "#":
                        screen.blit(self.img[12], self.rect)
                    elif up == "." and  down == "#" and left == "#" and  right == ".":
                        screen.blit(self.img[13], self.rect)
                    elif up == "#" and  down == "." and left == "#" and  right == ".":
                        screen.blit(self.img[14], self.rect)
                    elif up == "#" and  down == "." and left == "." and  right == "#":
                        screen.blit(self.img[15], self.rect)
                    else:
                        screen.blit(self.img[0], self.rect)

                self.rect[0] += gridsize
                i += 1            
            self.rect[0] = 0
            self.rect[1] += gridsize
            k += 1
        self.rect[1] = self.yOffset
    
    def checkCollision(self, rect, offset):
        self.offset = offset
        k = 0
        self.otherRect = rect
        self.rect[1] += self.offset
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
        self.img = pygame.image.load(GR_MYSHIP).convert_alpha()
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

def gameLoop(bgColor, level):
    global alive
    thisLevel = level
    turns = 0
    scrollSpeed = 2
    clock = pygame.time.Clock()
    while clock.tick(120):
        # Keyevents listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
        pressed = pygame.key.get_pressed()
        player.setSpeedX(pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT])
        player.setSpeedY(pressed[pygame.K_DOWN]-pressed[pygame.K_UP])

        # bounces from the wall
        if player.rect.left < 0 or player.rect.right > width:
            player.bounceX()
        if player.rect.top < 0 or player.rect.bottom > height:
            player.bounceY()

        # Player collision to walls
        if thisLevel.checkCollision(player.rect, turns * scrollSpeed):
            alive = False
            break
        
        #Player win
        if turns * scrollSpeed == thisLevel.length:
            break
        # Background update
        screen.fill(bgColor)
        stars.draw()
        thisLevel.draw(turns * scrollSpeed)

        # Player movement and draw
        player.move()
        screen.blit(player.img, player.rect)

        pygame.display.flip()
        bgColor = BLACK
        turns += 1

def showText(message):
    message = message
    font = pygame.font.Font('freesansbold.ttf', 48) 
    text = font.render(message, True, textColor)
    textRect = text.get_rect()  
    textRect.center = (width // 2, height // 2)
    screen.blit(text, textRect)
    pygame.display.flip()


# Main program
# Pygame initials
pygame.init()
screen = pygame.display.set_mode(size)  
currentLevel = 0

# Create background
stars = StarField(250)

i = 0
wallset_tech = images_tech
while i < len(wallset_tech):
    wallset_tech[i] = pygame.image.load(wallset_tech[i]).convert_alpha()
    i += 1
print(wallset_tech)

i = 0
wallset_stone = images_stone
while i < len(wallset_stone):
    wallset_stone[i] = pygame.image.load(wallset_stone[i]).convert_alpha()
    i += 1
print(wallset_stone)

# Create levels
level1 = Walls(level1_map, wallset_tech)
level2 = Walls(level2_map, wallset_stone)
level3 = Walls(level3_map, wallset_tech)

levels = [level1, level2, level3]


# Level loop
while True: 
    
    # Create player
    player = PlayerShip(width/2,height-100)
    alive = True

    # Play the level
    gameLoop(bgColor, levels[currentLevel])
   
    # Show level ending text
    if alive == False:
        showText("Kuolit")
    elif currentLevel >= len(levels)+1:
        showText("Kaikki kentat kayty lapi!")
    else:
        showText("Voitto!")
        currentLevel += 1  

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




