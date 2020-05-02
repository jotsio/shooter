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
    image = GR_HEART
    Rect = image.get_rect()
    Rect.y = height - Rect.height
    Rect.x = 0
    i = 0
    while i < amount:
        SCREEN.blit(image, Rect)
        Rect.x += Rect.width
        i += 1

# CLASSES
# -------
class NewEffect(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list):
        pygame.sprite.Sprite.__init__(self)
        effects_group.add(self)
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
        self.rect = self.rect.move(0, round(scroll_speed))
        # Change image
        self.image = self.animation[round(self.counter / self.delay_multiplier) - 1]
        self.counter += 1

# Ammunition
class NewShot(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy, graphics, animation, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = graphics
        group.add(self)
        self.animation = animation
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.alive = True
        self.speed = [0.0, speedy] 

    # Passive movement
    def update(self, level):

        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.rect, offset)
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
  
    def explode(self):
            explosion = NewEffect(self.rect.centerx, self.rect.centery, self.animation)
            snd_small_explo.play()

    def move(self):
        self.rect = self.rect.move(self.speed)

# Enemy class
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global enemy_ammo_group
        enemy_group.add(self)
        self.image_default = GR_ENEMYSHIP
        self.image = self.image_default
        self.animation = ANIM_ENEMYSHIP_BLINK
        self.animation_frame = 0
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(x, y)
        self.hit_points = 3
        self.shoot_timer = 0
        self.shoot_delay = 80
        self.blinking = False
        self.animation_frame = 0
        self.animation_delay = 4
        self.animation_counter = 0


    # Passive movement & collision detection
    def update(self, level):
        # Check if dead
        if self.hit_points <= 0:
            snd_enemy_death.play()
            explosion = NewEffect(self.rect.centerx, self.rect.centery, ANIM_ORANGEEXP)
            self.kill()

        # Check if outside area
        if self.rect.y < -gridsize * 2 or self.rect.y > height:
            self.kill()

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

        # Check collision ammo
        if pygame.sprite.spritecollideany(self, player_ammo_group):
            self.hit_points -= 1
            self.blinking = True

        # Check shooting delay
        if self.shoot_timer >= self.shoot_delay:
            self.shoot()
        else:
            self.shoot_timer += 1

    def move(self, scroll_speed):
        # Keep on scrolling
        self.rect = self.rect.move(0, round(scroll_speed))

    # Shooting
    def shoot(self):
        shot = NewShot(self.rect.centerx, self.rect.y + self.rect[3] + 8, 6.0, GR_AMMO_ENEMY, ANIM_PINKEXP, enemy_ammo_group)
        snd_laser_enemy.play()
        self.shoot_timer = 0 

# Player class
class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global player_ammo_group
        player_group.add(self)
        self.alive = True
        self.hit_points = 5
        self.hit_points_max = 6
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
        # Check if dead
        if self.hit_points <= 0:
            self.alive = False
            snd_player_death.play()
            player_group.remove(player)
            explosion = NewEffect(self.rect.centerx, self.rect.centery, ANIM_ORANGEEXP)

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
        if self.alive == True and level.checkCollision(self.getHitbox(), offset):
            self.hit_points = 0

        # Check collision to ammo
        if self.alive == True and pygame.sprite.spritecollideany(self, enemy_ammo_group):
            self.hit_points -= 1
            self.blinking = True

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

    def move(self):
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
            shot = NewShot(self.rect.centerx, self.rect.y-20, -10.0, GR_AMMO, ANIM_BLUEEXP, player_ammo_group)
            snd_laser.play()
            self.shoot_timer = 0 



# Main program
#-------------
# Pygame initials

# Global variables
framerate = 100
scroll_speed = 2
offset = 0
current_level = 0

# Title
pygame.display.set_caption("Luolalentely")
icon = GR_MYSHIP
pygame.display.set_icon(icon)

# Create player
player_group = pygame.sprite.Group()
player = PlayerShip(round(width/2),round(height-100))

# Main loop
while True: 
    # Play the level
    enemy_group = pygame.sprite.Group()
    player_ammo_group = pygame.sprite.Group()
    enemy_ammo_group = pygame.sprite.Group()
    effects_group = pygame.sprite.Group()
    offset = 0
    end_counter = 0
    stars = StarField(250)
    this_level = levels[current_level]
    clock = pygame.time.Clock()
    pygame.mixer.music.play(0)
    
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
        enemy_list = this_level.getEnemies(offset)
        if enemy_list:
            for i in enemy_list:
                enemy = EnemyShip(i[0], i[1])

        # Background update
        SCREEN.fill(color_bg_default)
        stars.draw(SCREEN)
        this_level.draw(offset, SCREEN)        

        # Draw all the objects
        player_group.draw(SCREEN)
        enemy_group.draw(SCREEN)
        player_ammo_group.draw(SCREEN)
        enemy_ammo_group.draw(SCREEN)
        effects_group.draw(SCREEN)

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
        current_level = 0
    else:
        showText("Kenttä läpäisty!")
        player.rect.x = player_start_x
        player.rect.y = player_start_y
        current_level += 1  

    pygame.event.clear()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.QUIT()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_RETURN:
            break




