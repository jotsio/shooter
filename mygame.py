import sys, pygame
import pygame.gfxdraw
import random
import time
from pygame.locals import *
from levels import *


# Global variables
alive = True
size = width, height = 1366, 768
gridsize = 64
player_safearea = 16
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_RED = 80, 0, 0
bgColor = BLACK
textColor = WHITE

#graphics
GR_MYSHIP = "assets/ship_default.png"
GR_AMMO = "assets/laserbeam.png"

#Load wall images
def loadWalls(tileset):
    i = 0
    images = tileset
    while i < len(images):
        images[i] = pygame.image.load(images[i]).convert_alpha()
        i += 1
    return images
        

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
    
    def checkCollision(self, obj_rect, offset):
        self.offset = offset
        k = 0
        self.rect[1] += self.offset
        #loop rows
        while k < len(self.map):
            #check one row of blocks and mark collision if wall exists
            i = 0
            while i < len(self.map[k]):
                if self.map[k][i] == "#" and self.rect.colliderect(obj_rect):
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

#Ammunition

class newShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(GR_AMMO).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.speed = [0.000, -10.000]  

    # Passive movement
    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.y < 0:
            self.kill()

#player class
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.startPos = [x, y]
        self.speed = [0.000, 0.000]  
        self.image = pygame.image.load(GR_MYSHIP).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.maxSpeedX = 4.0
        self.maxSpeedY = 2.0
        self.frictionX = 0.1
        self.frictionY = 0.1
        self.shoot_delay = 8
        self.shoot_timer = 0
    
    # Passive movement
    def update(self):
        if self.shoot_timer < self.shoot_delay:
            self.shoot_timer += 1
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

    def getHitbox(self):
        hitbox = (self.rect[0] + player_safearea, self.rect[1] + player_safearea, self.rect[2] - player_safearea * 2, self.rect[3] - player_safearea * 2)
        return hitbox

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

    def shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            shot = newShot(self.rect.x + 24, self.rect.y)
            player_group.add(shot)
            self.shoot_timer = 0


def levelLoop(bgColor, this_level):
    global alive
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
        if pressed[pygame.K_SPACE]:
            player.shoot()


        # bounces from the wall
        if player.rect.left < 0 or player.rect.right > width:
            player.bounceX()
        if player.rect.top < 0 or player.rect.bottom > height:
            player.bounceY()

        # Player collision to walls
        if this_level.checkCollision(player.getHitbox(), turns * scrollSpeed):
            alive = False
            break
        
        #Player win
        if turns * scrollSpeed == this_level.length:
            break
        # Background update
        screen.fill(bgColor)
        stars.draw()
        this_level.draw(turns * scrollSpeed)

        # Player movement and draw
        player_group.draw(screen)
        player_group.update()

 
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
#-------------
# Pygame initials
pygame.init()
# Title
pygame.display.set_caption("Luolalentely")
icon = pygame.image.load(GR_MYSHIP)
pygame.display.set_icon(icon)

# Define displays
pygame.FULLSCREEN
screen = pygame.display.set_mode(size)  

# Create stars on background
stars = StarField(250)

# Load level image sets
wallset_stone = loadWalls(images_stone)
wallset_tech = loadWalls(images_tech)

# Create levels
levels = [
    Walls(level1_map, wallset_tech), 
    Walls(level2_map, wallset_stone),  
    Walls(level3_map, wallset_tech)
    ]

currentLevel = 0

#level = SpriteWalls()

# Main loop
while True: 
    
    # Create player
    player = PlayerShip(width/2,height-100)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    alive = True

    # Play the level
    levelLoop(bgColor, levels[currentLevel])
   
    # Show level ending text
    if alive == False:
        showText("Kuolit!")
    elif currentLevel == (len(levels)-1):
        showText("HIENOA PELI LAPAISTY!")
        currentLevel = 0
    else:
        showText("Kentta lapaisty!")
        currentLevel += 1  

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




