import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from levels import *


# Global variables
framerate = 120
size = width, height = 1366, 768
gridsize = 64
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_RED = 80, 0, 0
bgColor = BLACK
textColor = WHITE


#graphics
GR_MYSHIP = "assets/ship_default.png"
GR_ENEMYSHIP = "assets/enemy1.png"
GR_AMMO = "assets/laserbeam.png"
ANIM_AMMO = ["assets/laserexp1.png", "assets/laserexp2.png", "assets/laserexp3.png", "assets/laserexp4.png"]

#Load wall images
def loadImageSet(image_list):
    i = 0
    while i < len(image_list):
        image_list[i] = pygame.image.load(image_list[i]).convert_alpha()
        i += 1
    return image_list

# Convert levels to lists
def levelToList(map):
    i = 0
    while i < len(map):
        map[i] = list(map[i])
        i += 1
    return map

#Walls class
class Walls:
    def __init__(self, map, tiles):
        self.map = levelToList(map)  
        self.img = tiles
        self.yOffset = -len(self.map) * gridsize
        self.length = -self.yOffset + height
        self.rect = pygame.Rect(0, self.yOffset, gridsize, gridsize) 

    def draw(self, offset):
        self.offset = offset
        k = 0
        self.rect[1] += round(self.offset)
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
    
    # Checks collision to walls for certain rectangle
    def checkCollision(self, obj_rect, offset):
        self.offset = offset
        k = 0
        self.rect[1] += round(self.offset)
        #loop rows
        while k < len(self.map):
            #check one row of blocks and mark collision if wall exists
            i = 0
            while i < len(self.map[k]):
                if self.map[k][i] == "#" and self.rect.colliderect(obj_rect):
                    self.rect[1] = self.yOffset
                    return (i, k)
                self.rect[0] += gridsize
                i += 1            
            self.rect[0] = 0
            self.rect[1] += gridsize
            k += 1
        self.rect[1] = self.yOffset
    
    # Removes defined wallblock from level
    def removeBlock(self, col, row):
        self.map[row][col] = "."

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

class newEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list):
        pygame.sprite.Sprite.__init__(self)
        self.animation = image_list
        self.image = self.animation[0]
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.delay_multiplier = 4
        self.lifetime = len(self.animation) * self.delay_multiplier
        self.counter = 0
        snd_small_explo.play()
    
    def update(self):
        # Check if dead
        if self.counter > self.lifetime:
            self.counter = 0
            self.kill()
        # Scoll down
        self.rect = self.rect.move(0, round(scrollSpeed))
        # Change image
        self.image = self.animation[round(self.counter / self.delay_multiplier) - 1]
        self.counter += 1


# Ammunition
class newShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(GR_AMMO).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x - self.rect.w / 2, y - self.rect.h / 2)
        self.ver_margin = 5
        self.hor_margin = 2
        self.speed = [0.000, -10.000] 
        snd_laser.play()

    # Passive movement
    def update(self, level):
        self.rect = self.rect.move(self.speed)
        # Check if outside area
        if self.rect.y < 0:
            self.kill()
        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.getHitbox(), turns * scrollSpeed)
        if hitted_block:
            self.kill()
            level.removeBlock(hitted_block[0], hitted_block[1])
            explosion = newEffect(self.rect.centerx, self.rect.centery, laser_explosion)
            effects_group.add(explosion)

    def getHitbox(self):
        hitbox = (self.rect[0] + self.hor_margin, self.rect[1] + self.ver_margin, self.rect[2] - self.ver_margin * 2, self.rect[3] - self.hor_margin * 2)
        return hitbox

# Enemy class
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global enemy_group
        self.alive = True
        self.image = pygame.image.load(GR_ENEMYSHIP).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
    
    # Passive movement & collision detection
    def update(self, level):
        # Keep on scrolling
        self.rect = self.rect.move(0, round(scrollSpeed))

    def die(self):
        self.kill()
        snd_death.play()
        explosion = newEffect(self.rect.centerx, self.rect.centery, laser_explosion)
        effects_group.add(explosion)

# Player class
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global player_group
        self.alive = True
        self.image = pygame.image.load(GR_MYSHIP).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.speedx = 0.0
        self.speedy = 0.0
        self.hor_margin = 8
        self.ver_margin = 15
        self.max_speedx = 4.0
        self.max_speedy = 2.0
        self.frictionX = 0.1
        self.frictionY = 0.1
        self.shoot_delay = 8
        self.shoot_timer = 0
    
    # Passive movement & collision detection
    def update(self, level):
        # Check shooting delay
        if self.shoot_timer < self.shoot_delay:
            self.shoot_timer += 1
        self.rect = self.rect.move(round(self.speedx), round(self.speedy))

        # bounces from outside the area
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = -self.speedx
        if self.rect.right > width:
            self.rect.right = width
            self.speedx = -self.speedx
        if self.rect.top < 0:
            self.rect.top = 0
            self.speedy = -self.speedy
        if self.rect.bottom > height:
            self.rect.bottom = height
            self.speedy = -self.speedy

        # Check collision to walls
        if self.alive == True and level.checkCollision(self.getHitbox(), turns * scrollSpeed):
            self.die()

        # Horizontal friction
        if self.speedx > 0 :
            self.speedx -= self.frictionX
        if self.speedx < 0 :
            self.speedx += self.frictionX
        # Vertical friction
        if self.speedy > 0 :
            self.speedy -= self.frictionY
        if self.speedy < 0 :
            self.speedy += self.frictionY

    def getHitbox(self):
        hitbox = (self.rect[0] + self.hor_margin, self.rect[1] + self.ver_margin, self.rect[2] - self.ver_margin * 2, self.rect[3] - self.hor_margin * 2)
        return hitbox

    # Vertical acceleration
    def setSpeedX(self, amount):
        self.speedx += amount
        if self.speedx > self.max_speedx :
            self.speedx = self.max_speedx
        if self.speedx < -self.max_speedx :
            self.speedx = -self.max_speedx

    # Horizontal acceleration
    def setSpeedY(self, amount):
        self.speedy += amount
        if self.speedy > self.max_speedy :
            self.speedy = self.max_speedy
        if self.speedy < -self.max_speedy :
            self.speedy = -self.max_speedy

    # Shooting
    def shoot(self):
        if player.alive == True and self.shoot_timer >= self.shoot_delay:
            shot = newShot(self.rect.centerx, self.rect.y)
            player_group.add(shot)
            self.shoot_timer = 0 

    def die(self):
        self.alive = False
        snd_death.play()
        player_group.remove(player)
        explosion = newEffect(self.rect.centerx, self.rect.centery, laser_explosion)
        effects_group.add(explosion)

def levelLoop(bgColor, this_level):
    global turns
    global scrollSpeed
    turns = 0
    scrollSpeed = 2.0
    clock = pygame.time.Clock()
    end_counter = 0
    enemy = EnemyShip(100, 100)
    enemy_group.add(enemy)

    while clock.tick(framerate):
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
         
       # Is player alive?
        if player.alive == False:
            player.speedx = 0.0
            player.speedy = 0.0
            if end_counter > framerate:
                break
            end_counter += 1

        # Is player reached the end of level?
        if turns * scrollSpeed == this_level.length:
            break

        # Background update
        screen.fill(bgColor)
        stars.draw()
        this_level.draw(turns * scrollSpeed)

        # Objects update
        player_group.update(this_level)
        enemy_group.update(this_level)
        effects_group.update()

        # Draw all the objects
        player_group.draw(screen)
        enemy_group.draw(screen)
        effects_group.draw(screen)

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
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) 
# Title
pygame.display.set_caption("Luolalentely")
icon = pygame.image.load(GR_MYSHIP)
pygame.display.set_icon(icon)

# Define displays
# pygame.FULLSCREEN
#screen = pygame.display.set_mode(size, FULLSCREEN | HWACCEL)  
screen = pygame.display.set_mode(size)  

# Create stars on background
stars = StarField(250)

# Load animations
laser_explosion = loadImageSet(ANIM_AMMO)

# Load sounds
snd_laser = pygame.mixer.Sound("sounds/laser1.ogg")
snd_laser.set_volume(0.15)
snd_death = pygame.mixer.Sound("sounds/player_destroyed.ogg")
snd_death.set_volume(0.8)
snd_small_explo = pygame.mixer.Sound("sounds/hit1.ogg")
snd_small_explo.set_volume(0.3)

# Load level image sets
wallset_stone = loadImageSet(images_stone)
wallset_tech = loadImageSet(images_tech)

# Create levels
levels = [
    Walls(level1_map, wallset_tech), 
    Walls(level2_map, wallset_stone),  
    Walls(level3_map, wallset_tech)
    ]

currentLevel = 0

# Main loop
while True: 
    
    # Create sprite groups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    effects_group = pygame.sprite.Group()

    # Create player
    player = PlayerShip(round(width/2),round(height-100))
    player_group.add(player)

    # Play the level
    levelLoop(bgColor, levels[currentLevel])
   
    # Show level ending text
    if player.alive == False:
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
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




