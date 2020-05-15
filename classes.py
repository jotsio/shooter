import pygame
from pygame.locals import *
from inits import *

# Create groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_ammo_group = pygame.sprite.Group()
enemy_ammo_group = pygame.sprite.Group()
effects_group = pygame.sprite.Group()

def collided(sprite, other):
    # Check if the hitboxes of the two sprites collide.
    return sprite.hitbox.colliderect(other.hitbox)

# Animated object class
class AnimObject():
    def __init__(self, imageset):
        self.imageset_default = imageset
        self.animation = self.imageset_default
        self.animation_duration = 0
        self.animation_delay = 2
        self.animation_frame = 0 
        self.image = self.animation[0]
        self.rect = self.image.get_rect() 
        self.ticks_in_frame = 4
        self.counter = 0

    def changeFrame(self):
        if self.counter % self.animation_delay == 0:
            if self.animation_frame >= len(self.animation):
                self.animation_frame = 0
            if self.animation_duration != 0 and self.counter > self.animation_duration:
                self.animation = self.imageset_default
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

class NewEffect(pygame.sprite.Sprite, AnimObject):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, imageset)
        effects_group.add(self)
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.lifetime = len(self.animation) * self.animation_delay
    
    def update(self, level, offset):
        # Check if dead
        if self.counter >= self.lifetime:
            self.kill()
        # Change image
        self.changeFrame()

    def move(self, scroll_speed):
        # Scoll down
        self.rect = self.rect.move(0, round(scroll_speed))

# Ammunition
class NewShotBeam(pygame.sprite.Sprite, AnimObject):
    def __init__(self, x, y, speedy, imageset, sec_imageset, group):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, imageset)
        group.add(self)
        self.explosion = sec_imageset
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.hitbox = self.rect
        self.speed = [0, speedy] 

    # Passive movement
    def update(self, level, offset):
        self.changeFrame()
        # Check collision, kill itself and create explosion
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block:
            # level.removeBlock(hitted_block[0], hitted_block[1])
            self.explode()
            self.kill()

        # Check if outside area
        elif self.rect.y < 0 or self.rect.y > level.height:
            self.kill()

        elif pygame.sprite.spritecollideany(self, enemy_group, collided):
            self.explode()
            self.kill()

        elif pygame.sprite.spritecollideany(self, player_group, collided):
            self.explode()
            self.kill()

    def explode(self):
            NewEffect(self.rect.centerx, self.rect.centery, self.explosion)
            snd_small_explo.play()

    def move(self, scroll_speed):
        self.rect = self.rect.move(self.speed)
        self.hitbox = self.hitbox.move(self.speed)
