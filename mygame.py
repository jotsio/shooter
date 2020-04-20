import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from levels import *

# HELPER FUNCTIONS
# ----------------
def loadImageSet(image_list):
    folder = IMG_FOLDER
    i = 0
    while i < len(image_list):
        image_list[i] = pygame.image.load(folder + image_list[i]).convert_alpha()
        i += 1
    return image_list

def loadImage(filename):
    folder = IMG_FOLDER
    filename = folder + filename
    image = pygame.image.load(filename).convert_alpha()
    return image

def loadSound(filename, volume):
    folder = SND_FOLDER
    filename = folder + filename
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    return sound

# Convert levels to lists
def levelToList(map):
    i = 0
    while i < len(map):
        map[i] = list(map[i])
        i += 1
    return map

# Show game titles
def showText(message):
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
        self.image = graphics
        self.animation = animation
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.alive = True
        self.speed = [0.0, speedy] 

    # Passive movement
    def update(self, level):

        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.rect)
        if hitted_block:
            level.removeBlock(hitted_block[0], hitted_block[1])
            self.explode()
            self.kill()
        # Check if outside area
        elif self.rect.y < 0 or self.rect.y > height:
            self.kill()

        elif pygame.sprite.spritecollideany(self, enemy_group):
            self.explode()
            self.kill()

        elif pygame.sprite.spritecollideany(self, player_group):
            self.explode()
            self.kill()
            
        self.rect = self.rect.move(self.speed)
  
    def explode(self):
            explosion = NewEffect(self.rect.centerx, self.rect.centery, self.animation)
            effects_group.add(explosion)
            snd_small_explo.play()

# Enemy class
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global enemy_ammo_group
        self.image_default = GR_ENEMYSHIP
        self.image = self.image_default
        self.animation = ANIM_ENEMYSHIP_BLINK
        self.animation_frame = 0
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.hit_points = 3
        self.damage = 0
        self.shoot_timer = 0
        self.shoot_delay = 100
        self.id = round(random.random() * 10000)
        self.blinking = False
        self.animation_frame = 0
        self.animation_delay = 4
        self.animation_counter = 0
 
    
    # Passive movement & collision detection
    def update(self, level):
        # Blinking
        if self.blinking == True:
            if self.animation_frame == len(self.animation):
                self.animation_frame = 0
                self.image = self.image_default
                self.animation_counter = 0
                self.blinking = False
            else:
                self.image = self.animation[self.animation_frame]
                if self.animation_counter == self.animation_delay:
                    self.animation_frame += 1
                    self.animation_counter = 0
                self.animation_counter +=1

        # Check if outside area
        if self.rect.y < -gridsize * 2 or self.rect.y > height:
            self.kill()

        # Check collision ammo
        if pygame.sprite.spritecollideany(self, player_ammo_group):
            print("Osuma!", self.id, "DMG:", self.damage, self.hit_points)
            self.damage += 1
            self.blinking = True
            if self.damage >= self.hit_points:
                self.die()

        # Check shooting delay
        if self.shoot_timer < self.shoot_delay:
            self.shoot_timer += 1
        self.shoot()

        # Keep on scrolling
        self.rect = self.rect.move(0, round(scrollSpeed))

    def die(self):
        snd_enemy_death.play()
        explosion = NewEffect(self.rect.centerx, self.rect.centery, ANIM_BLUEEXP)
        effects_group.add(explosion)
        self.kill()

    # Shooting
    def shoot(self):
        if self.shoot_timer >= self.shoot_delay:
            shot = NewShot(self.rect.centerx, self.rect.y + self.rect[3] + 8, 6.0, GR_AMMO_ENEMY, ANIM_PINKEXP)
            enemy_ammo_group.add(shot)
            snd_laser_enemy.play()
            self.shoot_timer = 0 


# Player class
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global player_ammo_group
        self.alive = True
        self.hit_points = 3
        self.damage = 0
        self.image_default = GR_MYSHIP
        self.animation = ANIM_MYSHIP_BLINK
        self.image = self.image_default
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
        self.blinking = False
        self.animation_frame = 0
        self.animation_delay = 4
        self.animation_counter = 0
    
    # Passive movement & collision detection
    def update(self, level):
        # Blinking
        if self.blinking == True:
            if self.animation_frame == len(self.animation):
                self.animation_frame = 0
                self.image = self.image_default
                self.animation_counter = 0
                self.blinking = False
            else:
                self.image = self.animation[self.animation_frame]
                if self.animation_counter == self.animation_delay:
                    self.animation_frame += 1
                    self.animation_counter = 0
                self.animation_counter +=1

        # Check collision to walls
        if self.alive == True and level.checkCollision(self.getHitbox()):
            self.die()

        # Check collision to ammo
        if self.alive == True and pygame.sprite.spritecollideany(self, enemy_ammo_group):
            self.damage += 1
            self.blinking = True
            if self.damage >= self.hit_points:
                self.die()

        # Check shooting delay
        if self.shoot_timer < self.shoot_delay:
            self.shoot_timer += 1

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

        # Move the player
        self.rect = self.rect.move(round(self.speedx), round(self.speedy))

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
            shot = NewShot(self.rect.centerx, self.rect.y-20, -10.0, GR_AMMO, ANIM_BLUEEXP)
            player_ammo_group.add(shot)
            snd_laser.play()
            self.shoot_timer = 0 

    def die(self):
        self.alive = False
        snd_player_death.play()
        player_group.remove(player)
        explosion = NewEffect(self.rect.centerx, self.rect.centery, ANIM_BLUEEXP)
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

# Asset folders for images and sounds
IMG_FOLDER = "assets/"
SND_FOLDER = "sounds/"

#graphics
GR_MYSHIP = loadImage("ship_default.png")
GR_ENEMYSHIP = loadImage("enemy_default.png")
GR_AMMO = loadImage("ammo_blue.png")
GR_AMMO_ENEMY = loadImage("ammo_pink.png")

# Load animations
ANIM_MYSHIP_BLINK = loadImageSet(["ship_hilight.png", "ship_default.png", "ship_hilight.png", "ship_default.png", "ship_hilight.png"])
ANIM_ENEMYSHIP_BLINK = loadImageSet(["enemy_hilight.png", "enemy_default.png", "enemy_hilight.png", "enemy_default.png", "enemy_hilight.png"])
ANIM_BLUEEXP = loadImageSet(["exp_blue1.png", "exp_blue2.png", "exp_blue3.png", "exp_blue4.png"])
ANIM_PINKEXP = loadImageSet(["exp_pink1.png", "exp_pink2.png", "exp_pink3.png", "exp_pink4.png"])

# Load level image sets
wallset_stone = loadImageSet(images_stone)
wallset_tech = loadImageSet(images_tech)

# Load sounds
snd_laser = loadSound("laser1.ogg", 0.15)
snd_laser_enemy = loadSound("laser2.ogg", 0.3)
snd_player_death = loadSound("defeated.ogg", 0.8)
snd_enemy_death = loadSound("hit1.ogg", 0.8)
snd_small_explo = loadSound("hit3.ogg", 0.3)

# Create levels
levels = [
    Walls(level1_map, wallset_tech), 
    Walls(level2_map, wallset_stone),  
    Walls(level3_map, wallset_tech),
    Walls(level4_map, wallset_tech)
    ]

# Title
pygame.display.set_caption("Luolalentely")
icon = GR_MYSHIP
pygame.display.set_icon(icon)

# Main loop
while True: 
    # Create stars on background
    stars = StarField(250)

    # Create sprite groups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    player_ammo_group = pygame.sprite.Group()
    enemy_ammo_group = pygame.sprite.Group()
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
        player_ammo_group.update(this_level)
        enemy_ammo_group.update(this_level)
        effects_group.update()

        # Draw all the objects
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_ammo_group.draw(SCREEN)
        enemy_ammo_group.draw(SCREEN)
        effects_group.draw(SCREEN)

        pygame.display.flip()
        color_bg_default = BLACK
        
        # Move the whole screen up one step
        offset += scrollSpeed

    # Show level ending text
    if player.alive == False:
        showText("Kuolit!")
    elif currentLevel == (len(levels)-1):
        showText("HIENOA, PELI LÄPÄISTY!")
        currentLevel = 0
    else:
        showText("Kenttä läpäisty!")
        currentLevel += 1  

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




