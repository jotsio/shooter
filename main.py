import sys, pygame
import pygame.gfxdraw
from pygame.locals import *
import random
import time
from levels import *
from inits import *

# Show game titles
def showText(message):
    font = pygame.font.Font('freesansbold.ttf', 48) 
    text = font.render(message, True, color_text)
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)
    SCREEN.blit(text, textRect)
    pygame.display.flip()

def showHearts(amount):
    image = GR_UI_HEART_DEFAULT
    Rect = image[0].get_rect()
    Rect.y = height - Rect.height
    Rect.x = 0
    i = 0
    while i < amount:
        SCREEN.blit(image[0], Rect)
        Rect.x += Rect.width
        i += 1


def collided(sprite, other):
    # Check if the hitboxes of the two sprites collide.
    return sprite.hitbox.colliderect(other.hitbox)

# CLASSES
# -------
# Animated object class
class AnimObject():
    def __init__(self, imageset):
        self.imageset_default = imageset
        self.animation = self.imageset_default
        self.animation_duration = 0
        self.animation_delay = 4
        self.animation_frame = 0 
        self.image = self.animation[0]
        self.rect = self.image.get_rect() 
        self.age = 0
        self.ticks_in_frame = 4

    def changeFrame(self):
        if self.age % self.ticks_in_frame == 0:
            if self.animation_frame >= len(self.animation):
                self.animation_frame = 0
            if self.animation_duration != 0 and self.age - self.animation_started > self.animation_duration:
                self.animation = self.imageset_default
                self.animation_frame = 0
            self.image = self.animation[self.animation_frame]
            if len(self.animation) > 1:
                self.animation_frame += 1
        self.age += 1
    
    def setAnimation(self, imageset, duration):
        self.animation_started = self.age
        self.animation = imageset
        self.animation_duration = duration 

class NewEffect(pygame.sprite.Sprite, AnimObject):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, imageset)
        effects_group.add(self)
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.lifetime = len(self.animation) * self.ticks_in_frame
    
    def update(self):
        # Check if dead
        if self.age > self.lifetime:
            self.kill()
        # Scoll down
        self.rect = self.rect.move(0, round(scroll_speed))
        # Change image
        self.changeFrame()
        self.age += 1

# Ammunition
class NewShot(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, graphics, animation, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics[0]
        group.add(self)
        self.animation = animation
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.hitbox = self.rect
        self.alive = True
        self.speed = [0, speedy] 

    # Passive movement
    def update(self, level):

        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block:
            # level.removeBlock(hitted_block[0], hitted_block[1])
            self.explode()
            self.kill()

        # Check if outside area
        elif self.rect.y < 0 or self.rect.y > height:
            self.kill()

        elif pygame.sprite.spritecollideany(self, enemy_group, collided):
            self.explode()
            self.kill()

        elif pygame.sprite.spritecollideany(self, player_group, collided):
            self.explode()
            self.kill()
  
    def explode(self):
            NewEffect(self.rect.centerx, self.rect.centery, self.animation)
            snd_small_explo.play()

    def move(self):
        self.rect = self.rect.move(self.speed)
        self.hitbox = self.hitbox.move(self.speed)

# Enemy class
class NewEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        global enemy_ammo_group
        enemy_group.add(self)
        self.image_default = features["image_default"]
        self.image = self.image_default[0]
        self.animation = features["animation_blink"]
        self.animation_frame = 0
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.hitbox = self.rect
        self.hit_points = features["hit_points"]
        self.shoot_delay = features["shoot_delay"]
        self.blinking = False
        self.animation_frame = 0
        self.animation_delay = 4
        self.animation_counter = 0
        self.hor_margin = -8
        self.ver_margin = -8
        self.speedx, self.speedy = features["initial_speed"]
        self.counter = 0
        self.last_shoot = self.counter
        self.type = features["type"]
        self.accuracy = 16

    # Passive movement & collision detection
    def update(self, level):
        global boss_alive
        # Check if dead
        if self.hit_points <= 0:
            snd_enemy_death.play()
            NewEffect(self.rect.centerx, self.rect.centery, GR_EFFECT_EXPLOSION_BIG)
            if self.type == "Boss":
                boss_alive = False
            self.kill()

        # Check if outside area
        if self.rect.y < -gridsize * 2 or self.rect.y > height:
            self.kill()

        # Blinking
        if self.blinking == True:
            if self.animation_frame == len(self.animation):
                self.animation_frame = 0
                self.image = self.image_default[0]
                self.animation_counter = 0
                self.blinking = False
            else:
                self.image = self.animation[self.animation_frame]
                if self.animation_counter == self.animation_delay:
                    self.animation_frame += 1
                    self.animation_counter = 0
                self.animation_counter +=1

        # Check collision ammo
        if pygame.sprite.spritecollideany(self, player_ammo_group, collided):
            self.hit_points -= 1
            self.blinking = True

        # Check collision to player
        if pygame.sprite.spritecollideany(self, player_group, collided):
            self.hit_points = 0

        # Check collision to walls
        if level.checkCollision(self.hitbox, offset) or self.rect.left <= 0 or self.rect.right >= width:
            self.speedx = -self.speedx

        # Check shooting delay
        if self.counter - self.last_shoot > self.shoot_delay and abs(player.rect.centerx - self.rect.centerx) < self.accuracy:
            self.shoot()
            self.last_shoot = self.counter
        
        self.counter += 1

    def move(self, scroll_speed):
        # Keep on scrolling
        self.rect = self.rect.move(self.speedx, self.speedy)
        self.rect = self.rect.move(0, round(scroll_speed))
        self.resetHitbox()
        
    def resetHitbox(self):
        # Align hitbox
        self.hitbox = self.rect
        self.hitbox = self.hitbox.inflate(self.hor_margin, self.ver_margin)

    # Shooting
    def shoot(self):
        NewShot(self.rect.centerx, self.rect.y + self.rect[3] + 8, 6.0, GR_AMMO_PINK_DEFAULT, GR_AMMO_PINK_EPXLOSION, enemy_ammo_group)
        snd_laser_enemy.play()
        self.shoot_timer = 0 

# Player class
class PlayerShip(pygame.sprite.Sprite, AnimObject):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, imageset = GR_PLAYER_BODY_DEFAULT)
        self.imageset_hilight = GR_PLAYER_BODY_BLINK
        self.imageset_up = GR_PLAYER_BODY_UP 
        global player_ammo_group
        self.start_x = x
        self.start_y = y
        self.alive = True
        self.hit_points = 5
        self.hit_points_max = 6
        self.speedx = 0.0
        self.speedy = 0.0
        self.hor_margin = -15
        self.ver_margin = -30
        self.max_speedx = 4.0
        self.max_speedy = 2.0
        self.frictionX = 0.2 
        self.frictionY = 0.2
        self.shoot_delay = 16
        self.shoot_timer = 0
        self.setStartPosition()
        player_group.add(self)
    
    # Set player to starting position on screen and initialize hitbox
    def setStartPosition(self):
        self.rect.x = 0
        self.rect.y = 0
        self.rect = self.rect.move(self.start_x, self.start_y)
        self.resetHitbox()
        
    # Passive movement & collision detection
    def update(self, level):
        # Check if dead
        if self.hit_points <= 0:
            self.alive = False
            snd_player_death.play()
            player_group.remove(player)
            NewEffect(self.rect.centerx, self.rect.centery, GR_EFFECT_EXPLOSION_BIG)

        # Check collision to walls
        if self.alive == True and level.checkCollision(self.hitbox, offset):
            self.hit_points = 0

        # Check collision to ammo
        if self.alive == True and pygame.sprite.spritecollideany(self, enemy_ammo_group, collided):
            self.hit_points -= 1
            self.setAnimation(self.imageset_hilight, 12)

        # Check collision to enemy
        if pygame.sprite.spritecollideany(self, enemy_group, collided):
            self.hit_points = 0

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
        
        # Set thruster animation if moved
        if self.speedy < -1.0:
            self.setAnimation(self.imageset_up, 4)

        # Change animation frame
        self.changeFrame()

        # Ensures that hitbox is following
        self.resetHitbox()


    def move(self):
        # Move the player
        self.rect = self.rect.move(round(self.speedx), round(self.speedy))
        self.resetHitbox()
        
    def resetHitbox(self):
        # Align hitbox
        self.hitbox = self.rect
        self.hitbox = self.hitbox.inflate(self.hor_margin, self.ver_margin)

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
            NewShot(self.rect.centerx, self.rect.y-20, -10.0, GR_AMMO_BLUE_DEFAULT, GR_AMMO_BLUE_EXPLOSION, player_ammo_group)
            snd_laser.play()
            self.shoot_timer = 0 



# Main program
#-------------
# Pygame initials

# Global variables
framerate = 100
basic_scroll_speed = 2
offset = 0
current_level = 0 
boss_alive = True

# Title
pygame.display.set_caption("Luolalentely")
icon = GR_PLAYER_BODY_DEFAULT
pygame.display.set_icon(icon[0])

# Create player
player_group = pygame.sprite.Group()
player = PlayerShip(player_start_x, player_start_y)

# Main loop
while True: 
    # Play the level
    enemy_group = pygame.sprite.Group()
    player_ammo_group = pygame.sprite.Group()
    enemy_ammo_group = pygame.sprite.Group()
    effects_group = pygame.sprite.Group()
    offset = 0
    scroll_speed = basic_scroll_speed
    end_counter = 0
    stars = StarField(250)
    this_level = levels[current_level]
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    boss_alive = True
    
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
            scroll_speed = 0  

        # Check if boss is dead         
        if boss_alive == False:
            if end_counter > framerate * 2:
                break
            end_counter += 1

        # Objects update
        player_group.update(this_level)
        enemy_group.update(this_level)
        player_ammo_group.update(this_level)
        enemy_ammo_group.update(this_level)
        effects_group.update()

        # Objects movement
        for each_enemy in enemy_group.sprites():
            each_enemy.move(scroll_speed)

        player.move()

        for each_enemy in player_ammo_group.sprites():
            each_enemy.move()

        for each_enemy in enemy_ammo_group.sprites():
            each_enemy.move()

        # Create enemies
        enemy_positions_list = this_level.getEnemies(offset)
        if enemy_positions_list:
            for i in enemy_positions_list:
                enemy = NewEnemy(i[0], i[1], i[2])

        # Background update
        SCREEN.fill(color_bg_default)
        stars.draw(SCREEN, 2)
        this_level.draw(offset, SCREEN)        

        # Draw all the objects
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_ammo_group.draw(SCREEN)
        enemy_ammo_group.draw(SCREEN)
        effects_group.draw(SCREEN)
        # Rectange for collision debugging
        #pygame.draw.rect(SCREEN, RED, player.hitbox, 1)

        # Show hearts of hitpoints
        showHearts(player.hit_points)

        # Update screen
        pygame.display.flip()
        
        # Move the whole screen up one step
        offset += scroll_speed

    # Show level ending text
    if player.alive == False:
        showText("Kuolit!")
        # Reset player
        player = PlayerShip(player_start_x, player_start_y)
        
    elif current_level == (len(levels)-1):
        showText("HIENOA, PELI LÄPÄISTY!")
        player.setStartPosition()
        current_level = 0
    else:
        showText("Kenttä läpäisty!")
        player.setStartPosition()
        boss_alive = True
        current_level += 1  

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




