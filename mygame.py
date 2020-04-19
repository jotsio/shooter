import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from levels import *

# HELPER FUNCTIONS
# ----------------
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


# Show game titles
def showText(message):
    message = message
    font = pygame.font.Font('freesansbold.ttf', 48) 
    text = font.render(message, True, textColor)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    SCREEN.blit(text, textRect)
    pygame.display.flip()

# CLASSES
# -------
# Stars class
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
            pygame.gfxdraw.pixel(SCREEN, self.x[i], int(self.y[i]), self.color[i])
            i += 1

#Walls class
class Walls:
    def __init__(self, map, tiles):
        global offset
        self.map = levelToList(map)  
        self.img = tiles
        self.start_point = -len(self.map) * gridsize
        self.rect = pygame.Rect(0, self.start_point, gridsize, gridsize) 

    def defineBlock(self, row, col):
        block = 0
        this = self.map[row][col]
        up = "#"
        down = "#"
        left = "#" 
        right = "#"
        if row > 0:
            up = self.map[row-1][col]
        if row < len(self.map)-1:
            down = self.map[row+1][col]
        if col > 0:
            left = self.map[row][col-1]
        if col < len(self.map[row])-1:
            right = self.map[row][col+1]
        if this == "#":
            if up == "#" and  down == "#" and left == "#" and  right == "#":
                block = 0
            elif up != "#" and  down != "#" and left != "#" and  right != "#":
                block = 1
            elif up != "#" and  down != "#" and left == "#" and  right == "#":
                block = 2
            elif up == "#" and  down == "#" and left != "#" and  right != "#":
                block = 3
            elif up != "#" and  down == "#" and left != "#" and  right != "#":
                block = 4
            elif up == "#" and  down != "#" and left != "#" and  right != "#":
                block = 5
            elif up != "#" and  down != "#" and left != "#" and  right == "#":
                block = 6
            elif up != "#" and  down != "#" and left == "#" and  right != "#":
                block = 7
            elif up != "#" and  down == "#" and left == "#" and  right == "#":
                block = 8
            elif up == "#" and  down != "#" and left == "#" and  right == "#":
                block = 9
            elif up == "#" and  down == "#" and left != "#" and  right == "#":
                block = 10
            elif up == "#" and  down == "#" and left == "#" and  right != "#":
                block = 11
            elif up != "#" and  down == "#" and left != "#" and  right == "#":
                block = 12
            elif up != "#" and  down == "#" and left == "#" and  right != "#":
                block = 13
            elif up == "#" and  down != "#" and left == "#" and  right != "#":
                block = 14
            elif up == "#" and  down != "#" and left != "#" and  right == "#":
                block = 15
            else:
                block = 0
        return block

    def draw(self):
        k = 0
        self.rect.y += offset
        #loop rows
        
        while k < len(self.map):
            #draw one row of blocks and draw graphics if wall exists
            if self.rect.y >= -gridsize and self.rect.y <= height:
                i = 0 
                while i < len(self.map[k]):
                    # Draw right block on screen
                    if self.map[k][i] == "#":
                        SCREEN.blit(self.img[self.defineBlock(k,i)], self.rect)
                    # create enemy on screen
                    if self.map[k][i] == "X" and self.rect.y == -gridsize:
                        enemy = EnemyShip(self.rect.x, self.rect.y)
                        enemy_group.add(enemy)
                    # select which wall asset to use
                    self.rect.x += gridsize
                    i += 1
                self.rect.x = 0
            k += 1
            self.rect.y += gridsize
        self.rect.y = self.start_point
    
    # Checks collision to walls for certain rectangle
    def checkCollision(self, obj_rect):
        k = 0
        self.rect.y += offset
        #loop rows
        while k < len(self.map):
            #check one row of blocks and mark collision if wall exists
            if self.rect.y >= -gridsize and self.rect.y <= height:
                i = 0
                while i < len(self.map[k]):
                    if self.map[k][i] == "#":
                        if self.rect.colliderect(obj_rect):
                            self.rect.y = self.start_point
                            return (i, k)
                    self.rect.x += gridsize
                    i += 1            
                self.rect.x = 0
            k += 1
            self.rect.y += gridsize
        self.rect.y = self.start_point

    # Removes defined wallblock from level
    def removeBlock(self, col, row):
        self.map[row][col] = "."


class NewEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list):
        pygame.sprite.Sprite.__init__(self)
        self.animation = image_list
        self.image = self.animation[0]
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.delay_multiplier = 4
        self.lifetime = len(self.animation) * self.delay_multiplier
        self.counter = 0
    
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
class NewShot(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, graphics, animation):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(graphics).convert_alpha()
        self.animation = animation
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.speed = [0.0, speedy] 

    # Passive movement
    def update(self, level):
        self.rect = self.rect.move(self.speed)
        # Check if outside area
        if self.rect.y < 0 or self.rect.y > height:
            self.kill()
        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.rect)
        if hitted_block:
            self.kill()
            level.removeBlock(hitted_block[0], hitted_block[1])
            explosion = NewEffect(self.rect.centerx, self.rect.centery, self.animation)
            effects_group.add(explosion)
            snd_small_explo.play()

# Enemy class
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global enemy_group
        self.image = pygame.image.load(GR_ENEMYSHIP).convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.shoot_timer = 0
        self.shoot_delay = 100
    
    # Passive movement & collision detection
    def update(self, level):
        # Keep on scrolling
        self.rect = self.rect.move(0, round(scrollSpeed))
        
        # Check if outside area
        if self.rect.y < -gridsize * 2 or self.rect.y > height:
            self.kill()

        # Check collision to enemy or enemy ammo
        if pygame.sprite.spritecollideany(self, player_group):
            self.die()

        # Check shooting delay
        if self.shoot_timer < self.shoot_delay:
            self.shoot_timer += 1
        self.shoot()

    def die(self):
        snd_enemy_death.play()
        explosion = NewEffect(self.rect.centerx, self.rect.centery, laser_explosion)
        effects_group.add(explosion)
        self.kill()

    # Shooting
    def shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            shot = NewShot(self.rect.centerx, self.rect.y + self.rect[3], 6.0, GR_AMMO_ENEMY, ANIM_PINKEXP)
            enemy_group.add(shot)
            snd_laser_enemy.play()
            self.shoot_timer = 0 


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
        if self.alive == True and level.checkCollision(self.getHitbox()):
            self.die()

        # Check collision to enemy or enemy ammo
        if self.alive == True and pygame.sprite.spritecollideany(self, enemy_group):
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
        hitbox = (self.rect.x + self.hor_margin, self.rect.y + self.ver_margin, self.rect[2] - self.ver_margin * 2, self.rect[3] - self.hor_margin * 2)
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
    def shoot(self, key):
        if self.alive == True and self.shoot_timer >= self.shoot_delay and key == True:
            shot = NewShot(self.rect.centerx, self.rect.y, -10.0, GR_AMMO, ANIM_BLUEEXP)
            player_group.add(shot)
            snd_laser.play()
            self.shoot_timer = 0 

    def die(self):
        self.alive = False
        snd_player_death.play()
        player_group.remove(player)
        explosion = NewEffect(self.rect.centerx, self.rect.centery, laser_explosion)
        effects_group.add(explosion)

# Main program
#-------------
# Pygame initials
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) 

# Global variables
framerate = 100
scrollSpeed = 2
offset = 0
currentLevel = 0
size = width, height = 1366, 768
gridsize = 64

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
DARK_GREY = 64, 64, 64
DARK_RED = 80, 0, 0
color_bg_default = BLACK
textColor = WHITE

# Define displays
#pygame.FULLSCREEN
#SCREEN = pygame.display.set_mode(size, FULLSCREEN | HWACCEL)  
SCREEN = pygame.display.set_mode(size)  

#graphics
GR_MYSHIP = "assets/ship_default.png"
GR_ENEMYSHIP = "assets/enemy1.png"
GR_AMMO = "assets/ammo_blue.png"
GR_AMMO_ENEMY = "assets/ammo_pink.png"
ANIM_BLUEEXP = ["assets/exp_blue1.png", "assets/exp_blue2.png", "assets/exp_blue3.png", "assets/exp_blue4.png"]
ANIM_PINKEXP = ["assets/exp_pink1.png", "assets/exp_pink2.png", "assets/exp_pink3.png", "assets/exp_pink4.png"]

# Load animations
laser_explosion = loadImageSet(ANIM_BLUEEXP)
laser2_explosion = loadImageSet(ANIM_PINKEXP)

# Load level image sets
wallset_stone = loadImageSet(images_stone)
wallset_tech = loadImageSet(images_tech)

# Load sounds
snd_laser = pygame.mixer.Sound("sounds/laser1.ogg")
snd_laser.set_volume(0.15)
snd_laser_enemy = pygame.mixer.Sound("sounds/laser2.ogg")
snd_laser_enemy.set_volume(0.3)
snd_player_death = pygame.mixer.Sound("sounds/defeated.ogg")
snd_player_death.set_volume(0.8)
snd_enemy_death = pygame.mixer.Sound("sounds/hit1.ogg")
snd_enemy_death.set_volume(0.8)
snd_small_explo = pygame.mixer.Sound("sounds/hit3.ogg")
snd_small_explo.set_volume(0.3)

# Create levels
levels = [
    Walls(level1_map, wallset_tech), 
    Walls(level2_map, wallset_stone),  
    Walls(level3_map, wallset_tech),
    Walls(level4_map, wallset_tech)
    ]

# Title
pygame.display.set_caption("Luolalentely")
icon = pygame.image.load(GR_MYSHIP)
pygame.display.set_icon(icon)

# Main loop
while True: 
    # Create stars on background
    stars = StarField(250)

    # Create sprite groups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    effects_group = pygame.sprite.Group()

    # Create player
    player = PlayerShip(round(width/2),round(height-100))
    player_group.add(player)

    # Play the level
    end_counter = 0
    offset = 0
    this_level = levels[currentLevel]
    clock = pygame.time.Clock()
    
    while clock.tick(framerate):
        # Keyevents listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        pressed = pygame.key.get_pressed()
        player.setSpeedX(pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT])
        player.setSpeedY(pressed[pygame.K_DOWN]-pressed[pygame.K_UP])
        player.shoot(pressed[pygame.K_SPACE])
         
       # Is player alive?
        if player.alive == False:
            player.speedx = 0.0
            player.speedy = 0.0
            if end_counter > framerate:
                break
            end_counter += 1

        # Is player reached the end of level?
        if offset == -this_level.start_point:
            break

        # Background update
        SCREEN.fill(color_bg_default)
        stars.draw()
        this_level.draw()

        # Objects update
        player_group.update(this_level)
        enemy_group.update(this_level)
        effects_group.update()

        # Draw all the objects
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        effects_group.draw(SCREEN)

        pygame.display.flip()
        color_bg_default = BLACK
        
        # Move the whole screen up one step
        offset += scrollSpeed

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




