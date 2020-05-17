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

class Solid():
    def __init__(self, rect, collision_group):
        self.hitbox = rect
        self.collision_group = collision_group
        self.hitpoints = 1

    def outsideArea(self, level):
        # Check if outside area
        result = False
        if self.hitbox.bottom < 0 or self.hitbox.top > level.height:
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

    def collisionToEnemy(self):
        return pygame.sprite.spritecollideany(self, self.collision_group, self.collided)

    def explode(self, animation, sound):
        NewEffect(self.hitbox.centerx, self.hitbox.centery, animation)
        sound.play()

class NewEffect(pygame.sprite.Sprite, AnimObject):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, imageset)
        effects_group.add(self)
        self.rect = self.image.get_rect() 
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.lifetime = len(self.animation) * self.animation_delay
    
    def update(self, level, offset):
        # Erase if lifetime spent
        if self.counter >= self.lifetime:
            self.kill()
        # Change image
        self.changeFrame()

    def move(self, scroll_speed):
        # Scoll down
        self.rect = self.rect.move(0, round(scroll_speed))


# Ammunition new
class AmmoSingle(pygame.sprite.Sprite, AnimObject, Solid):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        AnimObject.__init__(self, features["imageset_default"])
        Solid.__init__(self, self.rect, features["collision_group"])
        features["own_group"].add(self)
        self.features = features
        # Centrify position
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.hitbox = self.rect
        # Vertical speed
        self.speed = [0, features["speedy"]]
        self.energy = features["energy"]
        features["sound_launch"].play()

    def update(self, level, offset):
        if self.destroyed() == True:
            self.explode(self.features["imageset_explosion"], self.features["sound_explosion"])
            self.kill()
        # Disappear if outside the area
        if self.outsideArea(level):
            self.kill()
        # Explode if collided to level walls
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block:
            # level.removeBlock(hitted_block[0], hitted_block[1])
            self.hitpoints = 0
        # Explode if collided to collision group
        elif self.collisionToEnemy():
            self.hitpoints = 0
        # Updates possible animation
        self.changeFrame()

    def explode(self, animation, sound):
        NewEffect(self.rect.centerx, self.rect.centery, animation)
        sound.play()

    def move(self, scroll_speed):
        self.rect = self.rect.move(self.speed)
        self.hitbox = self.hitbox.move(self.speed)

# Ammo types
feat_player_beam_default = {
    "own_group": player_group,
    "collision_group": enemy_group,
    "imageset_default": GR_AMMO_BLUE_DEFAULT,
    "imageset_explosion": GR_AMMO_BLUE_EXPLOSION,
    "sound_launch": snd_laser,
    "sound_explosion": snd_small_explo,
    "speedy": -10,
    "energy": 10,  
}

feat_player_flame = {
    "own_group": player_group,
    "collision_group": enemy_group,
    "imageset_default": GR_EFFECT_EXPLOSION_BIG,
    "imageset_explosion": GR_EFFECT_EXPLOSION_BIG,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_small_explo,
    "speedy": -8,
    "energy": 2,  
}

feat_enemy_beam_default = {
    "own_group": enemy_group,
    "collision_group": player_group,
    "imageset_default": GR_AMMO_PINK_DEFAULT,
    "imageset_explosion": GR_AMMO_PINK_EPXLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_laser_enemy,
    "speedy": 8,
    "energy": 2,  
}