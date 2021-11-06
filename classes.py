import pygame
import math
import random
from pygame.locals import *
from inits import *

score = 0

# Create groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_ammo_group = pygame.sprite.Group()
enemy_ammo_group = pygame.sprite.Group()
effects_group = pygame.sprite.Group()

def checkBosses():
    result = False
    for i in enemy_group:
        if i.type == "Boss":
            return True
    return result 

# CLASSES
# -------
# Base object class
class Base():
    def __init__(self, x, y, imageset, group):
        group.add(self)
        self.hostile_group = []
        self.imageset_default = imageset
        self.animation = self.imageset_default
        self.animation_duration = 0
        self.animation_frame = 0 
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.hor_margin = 0
        self.ver_margin = 0
        self.alignHitBox(self.rect) 
        self.ticks_in_frame = 4
        self.counter = 0
        self.hitpoints = 1
        self.max_speedx = 32.0
        self.max_speedy = 32.0
        self.speed = (0.0, 0.0)
        self.orientation = (0.0, 0.0)
        self.hit_energy = 0
        self.destroys_walls = False
        self.killed = False
        self.score = 1
        

    def changeFrame(self):
        if self.counter % self.ticks_in_frame == 0:
            if self.animation_frame >= len(self.animation):
                self.animation_frame = 0
            if self.animation_duration != 0 and self.counter > self.animation_duration:
                self.animation = self.imageset_default
                self.animation_duration =  0
                self.animation_frame = 0
                self.counter = 0
            self.image = self.animation[self.animation_frame]
            if len(self.animation) > 1:
                self.animation_frame += 1
        self.counter += 1
    
    def setAnimation(self, imageset, duration):
        self.animation = imageset
        self.animation_duration = duration 
        self.counter = 0

    def alignHitBox(self, rect):
        self.hitbox = rect
        self.hitbox = self.hitbox.inflate(self.hor_margin, self.ver_margin)

    def alignRect(self, hitbox):
        self.rect.centerx = hitbox.centerx
        self.rect.centery = hitbox.centery

    def outsideArea(self, level):
        # Check if outside area
        result = False
        if self.hitbox.bottom < update_offset_up or self.hitbox.top > level.height + update_offset_down:
            result = True
        elif self.hitbox.right < 0 or self.hitbox.left > level.width:
            result = True
        return result

    def destroyed(self):
        if self.hitpoints <= 0:
            return True
        else:
            return False

    def collided(self, sprite, other):
        # Check if the hitboxes of the two sprites collide.
        return sprite.hitbox.colliderect(other.hitbox)

    def getCollisionDamage(self, group):
        for subject in group:
            if self.collided(self, subject):
                return subject.hit_energy

    def destroyWall(self, level, row, col, wall_rect):
        level.removeBlock(row, col)
        snd_wall_destroy.play()
        level.createPieces(wall_rect.centerx, wall_rect.centery, 10)

    def bounceFromWalls(self, level, offset):
        # Check collision to walls
        if level.checkCollision(self.hitbox, offset):
            self.speed = (-self.speed[0], self.speed[1]) 

    def bounceFromSides(self, level, offset):
        # Keeps object horizontally on screen
        if self.hitbox.left < 0:
            while self.hitbox.left < 0:
                self.rect.left += 1
                self.alignHitBox(self.rect)
            self.speed = (-self.speed[0], self.speed[1]) 
        if self.hitbox.right > width:
            while self.hitbox.right > width: 
                self.rect.right -= 1
                self.alignHitBox(self.rect)
            self.speed = (-self.speed[0], self.speed[1]) 

    def bounceFromRect(self, obj_rect):
        if obj_rect != None:
            dx = self.hitbox.centerx - obj_rect.centerx
            dy = self.hitbox.centery - obj_rect.centery
            if abs(dx) >= abs(dy):
                if dx <= 0:
                    self.hitbox.right = obj_rect.left
                if dx > 0:
                    self.hitbox.left = obj_rect.right
                self.speed = (-self.speed[0], self.speed[1])     
            else:
                if dy <= 0:
                    self.hitbox.bottom = obj_rect.top
                if dy > 0:
                    self.hitbox.top = obj_rect.bottom
                self.speed = (self.speed[0], -self.speed[1])   
            self.alignRect(self.hitbox)

    def bounceFromTopandBottom(self, level):
            sx, sy = self.speed
            if self.rect.top < 0:
                self.rect.top = 0
                sy = -sy
            if self.rect.bottom > level.height:
                self.rect.bottom = level.height
                sy = -sy
            self.speed = (sx, sy)

    def bounceStronglyFromRect(self, obj_rect):
        if obj_rect != None:
            power = 6.0
            sx, sy = self.speed
            dx = obj_rect.centerx - self.hitbox.centerx
            dy = obj_rect.centery - self.hitbox.centery
            if abs(dx) >= abs(dy):
                if dx <= 0:
                    self.hitbox.left = obj_rect.right
                    sx += power
                else:
                    self.hitbox.right = obj_rect.left
                    sx -= power

            else:
                if dy <= 0:
                    self.hitbox.top = obj_rect.bottom
                    sy += power
                else:
                    self.hitbox.bottom = obj_rect.top
                    sy -= power

            self.speed = (sx, sy)  
            self.alignRect(self.hitbox)

    def collisionToEnemy(self):
        return pygame.sprite.spritecollideany(self, self.hostile_group, self.collided)

    def applyFriction(self, x_friction, y_friction):
        # Horizontal friction
        sx, sy = self.speed
        if sx > 0.0 :
            sx -= x_friction
        if sx < 0.0 :
            sx += x_friction

        # Vertical friction
        if sy > 0.0 :
            sy -= y_friction
        if sy < 0.0 :
            sy += y_friction
        self.speed = (sx, sy)

    def sprinkle(self, speed):
        x = (random.random()-0.5) * speed
        y = (random.random()-0.5) * speed/2
        self.speed = (x, y)

    def move(self, scroll_speed):
        self.rect = self.rect.move(self.speed)
        self.rect = self.rect.move(0.0, scroll_speed)
        self.alignHitBox(self.rect)

    def explode(self, animation, sound):
        NewEffect(self.hitbox.centerx, self.hitbox.centery, animation)
        sound.play()

class NewEffect(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, imageset, effects_group)
        self.rect = self.rect.move(round(-self.rect.w / 2), -round(self.rect.h / 2))
        self.lifetime = len(self.animation) * self.ticks_in_frame
    
    def update(self, level, offset):
        # Erase if lifetime spent
        if self.counter >= self.lifetime:
            self.kill()
        
        # Update animation
        self.changeFrame()

class NewParticleEffect(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, imageset, effects_group)
        random_image = random.randrange(1, len(self.animation))-1
        self.image = self.animation[random_image]
        self.lifetime = random.randrange(10, 50)
        self.rect = self.rect.move(random.randrange(-16, 16), random.randrange(-16, 16))
        self.sprinkle(10)
    
    def update(self, level, offset):
        # Erase if lifetime spent
        if self.counter >= self.lifetime:
            self.kill()
        self.counter += 1
        
    

    