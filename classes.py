import pygame
import math
import random
from levels import *
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
        self.ticks_in_frame = 4
        self.counter = 0
        self.hor_margin = 0
        self.ver_margin = 0
        self.alignHitBox(self.rect)
        self.hitpoints = 1
        self.max_speedx = 32.0
        self.max_speedy = 32.0
        self.speed = (0.0, 0.0)

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

    def outsideArea(self, level):
        # Check if outside area
        result = False
        if self.hitbox.bottom < -2560 or self.hitbox.top > level.height + 256:
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

    def bounceFromWalls(self, level, offset):
        # Check collision to walls
        if level.checkCollision(self.hitbox, offset) or self.hitbox.left <= 0 or self.hitbox.right >= width:
            self.speed = (-self.speed[0], self.speed[1]) 

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
        self.rect = self.rect.move(round(x - self.rect.w / 2), y - round(self.rect.h / 2))
        self.lifetime = len(self.animation) * self.ticks_in_frame
    
    def update(self, level, offset):
        # Erase if lifetime spent
        if self.counter >= self.lifetime:
            self.kill()
        
        # Update animation
        self.changeFrame()

class Collectable(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, imageset):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, imageset, effects_group)
        self.hostile_group = player_group
        # Centrify position
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.alignHitBox(self.rect)
        self.frequency = 80
        self.amplitude = 2
        self.pivot = self.rect
        self.counter = round(random.random() * self.frequency)
        self.wave_y = 0.0
        self.wave_x = 0.0
        self.sprinkle(12)
    
    def update(self, level, offset):
        # Explode if collided to collision group
        if self.collisionToEnemy():
            self.hitpoints = 0
            snd_coin.play()
        if self.destroyed() == True:
            self.kill()
        
        self.bounceFromWalls(level, offset)

        # Disappear if outside the area
        if self.outsideArea(level):
            self.kill()
        
        # Wave up and down
        self.wave_y = round(self.amplitude * math.sin(2 * math.pi * (self.counter / self.frequency)))

        # Update animation
        self.changeFrame()
        self.applyFriction(0.1, 0.1)

    def move(self, scroll_speed):
        self.pivot = self.pivot.move(self.speed)
        self.pivot = self.pivot.move(0.0, scroll_speed)
        self.rect = self.pivot
        self.rect.y = self.pivot.y + self.wave_y
        self.alignHitBox(self.rect)

# Ammunition new
class AmmoBasic(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, features["imageset_default"], features["own_group"])
        self.hostile_group = features["enemy_group"]
        self.features = features
        # Centrify position
        self.rect = self.rect.move(round(x - self.rect.w / 2), round(y - self.rect.h / 2))
        self.alignHitBox(self.rect)
        # Vertical speed
        self.speed = (0.0, features["speedy"])
        self.energy = features["energy"]
        features["sound_launch"].play()

    def update(self, level, offset):

        # Explode if collided to level walls
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block:
            if self.energy > 10: 
                level.removeBlock(hitted_block[0], hitted_block[1])
            self.hitpoints = 0
        # Explode if collided to collision group
        elif self.collisionToEnemy():
            self.hitpoints = 0
        # Updates possible animation

        if self.destroyed() == True:
            self.explode(self.features["imageset_explosion"], self.features["sound_explosion"])
            self.kill()
        # Disappear if outside the area
        if self.outsideArea(level):
            self.kill()

        self.changeFrame()

    def explode(self, animation, sound):
        NewEffect(self.rect.centerx, self.rect.centery, animation)
        sound.play()

class AmmoRocket(AmmoBasic):
    def move(self, scroll_speed):
        self.rect = self.rect.move(self.speed)
        self.rect = self.rect.move(0, scroll_speed)
        self.alignHitBox(self.rect)
        sy = self.speed[1]
        if sy > -10.0:    
            sy += sy
        else:
            sy = -10.0
        self.speed = (self.speed[0], sy) 

class AmmoFlame(AmmoBasic):
    def update(self, level, offset):

        # Explode if collided to level walls
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block:
            if self.energy > 10: 
                level.removeBlock(hitted_block[0], hitted_block[1])
            self.hitpoints = 0
        # Explode if collided to collision group
        elif self.collisionToEnemy():
            self.hitpoints = 0
        # Updates possible animation

        if self.destroyed() == True:
            self.explode(self.features["imageset_explosion"], self.features["sound_explosion"])
            self.kill()
        # Disappear if outside the area
        if self.outsideArea(level):
            self.kill()
        
        if self.counter >= len(self.animation) * self.ticks_in_frame:
            self.kill()

        self.applyFriction(0.0, 0.2)
        self.changeFrame()

# Player class
class PlayerShip(pygame.sprite.Sprite, Base):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, GR_PLAYER_BODY_DEFAULT, player_group)
        self.hostile_group = enemy_ammo_group
        self.hor_margin = -15
        self.ver_margin = -30
        self.imageset_hilight = GR_PLAYER_BODY_BLINK
        self.imageset_up = GR_PLAYER_BODY_UP 
        self.start_x = x
        self.start_y = y
        self.alive = True
        self.hitpoints = 5
        self.hitpoints_max = 6
        self.max_speedx = 4.0
        self.max_speedy = 3.0
        self.frictionX = 0.2 
        self.frictionY = 0.2
        self.setStartPosition()
        self.weapon = WeaponSingle(feat_player_beam_default)
    
    # Set player to starting position on screen and initialize hitbox
    def setStartPosition(self):
        self.rect.x = 0
        self.rect.y = 0
        self.rect = self.rect.move(self.start_x, self.start_y)
        self.alignHitBox(self.rect)
        
    # Passive movement & collision detection
    def update(self, level, offset):
        sx, sy = self.speed
        # Check if dead        
        if self.alive == True:
            if self.destroyed() == True:
                self.alive = False
                self.explode(GR_EFFECT_EXPLOSION_BIG, snd_player_death)
                player_group.remove(self)
            
            # Check collision to walls
            if level.checkCollision(self.hitbox, offset):
                self.hitpoints = 0
            # Check collision to ammo
            if self.collisionToEnemy():
                self.hitpoints -= 1
                self.setAnimation(self.imageset_hilight, 12)
            # Check collision to enemy
            if pygame.sprite.spritecollideany(self, enemy_group, self.collided):
                self.hitpoints = 0

            # Update shooting delay
            self.weapon.shoot_timer += 1

            # bounces from outside the area
            if self.rect.left < 0:
                self.rect.left = 0
                sx = -sx
            if self.rect.right > width:
                self.rect.right = width
                sx = -sx
            if self.rect.top < 0:
                self.rect.top = 0
                sy = -sy
            if self.rect.bottom > level.height:
                self.rect.bottom = level.height
                sy = -sy
            self.speed = (sx, sy)

            # Set thruster animation if moved
            if self.speed[1] < -1.0:
                self.setAnimation(self.imageset_up, 4)

            # Apply Friction
            self.applyFriction(self.frictionX, self.frictionY)

            # Change animation frame
            self.changeFrame()

            # Ensures that hitbox is following
            self.alignHitBox(self.rect)


    def move(self, scroll_speed): 
        # Move the player
        self.rect = self.rect.move(self.speed)
        self.alignHitBox(self.rect)

    def setSpeed(self, acc_x, acc_y):
        sx, sy = self.speed
        sx += acc_x
        sy += acc_y
        if sx > self.max_speedx :
            sx = self.max_speedx
        if sx < -self.max_speedx :
            sx = -self.max_speedx
        if sy > self.max_speedy :
            sy = self.max_speedy
        if sy < -self.max_speedy :
            sy = -self.max_speedy
        self.speed = (sx, sy)

    # Change a weapon
    def changeWeapon(self, key):
        if key[pygame.K_1] == True:
            self.weapon = WeaponSingle(feat_player_beam_default)
        if key[pygame.K_2] == True:
            self.weapon = WeaponDouble(feat_player_beam_default)
        if key[pygame.K_3] == True:
            self.weapon = WeaponMinigun(feat_player_beam_default)
        if key[pygame.K_4] == True:
            self.weapon = WeaponLauncher(feat_player_rocket)
        if key[pygame.K_5] == True:
            self.weapon = WeaponThrower(feat_player_flame)

    # Change a weapon
    def getWeapon(self, key):
        if key == 1:
            self.weapon = WeaponSingle(feat_player_beam_default)
        if key == 2:
            self.weapon = WeaponDouble(feat_player_beam_default)
        if key == 3:
            self.weapon = WeaponMinigun(feat_player_beam_default)
        if key == 4:
            self.weapon = WeaponLauncher(feat_player_rocket)
        if key == 5:
            self.weapon = WeaponThrower(feat_player_flame)

    # Shooting
    def shoot(self, key):
        if self.alive == True and key == True:
            self.weapon.launch(self.rect.centerx, self.rect.y)


# Weapons
class WeaponBase():
    def __init__(self, ammo):
        self.ammo = ammo
        self.shoot_delay = 0
        self.power = 1.0
        self.shoot_timer = 0
    
    def setFirerate(self, rpm):
        self.shoot_delay = round(100 * 60 / rpm)

class WeaponSingle(WeaponBase):
    def __init__(self, ammo):
        WeaponBase.__init__(self, ammo)
        self.setFirerate(600)

    def launch(self, x, y):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, self.ammo)
            self.shoot_timer = 0 

class WeaponDouble(WeaponBase):
    def __init__(self, ammo):
        WeaponBase.__init__(self, ammo)
        self.setFirerate(450)

    def launch(self, x, y):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x - 16, y, self.ammo)
            AmmoBasic(x + 16, y, self.ammo)
            self.shoot_timer = 0 

class WeaponMinigun(WeaponBase):
    def __init__(self, ammo):
        WeaponBase.__init__(self, ammo)
        self.setFirerate(1200)

    def launch(self, x, y):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, self.ammo)
            self.shoot_timer = 0 

class WeaponLauncher(WeaponBase):
    def __init__(self, ammo):
        WeaponBase.__init__(self, ammo)
        self.setFirerate(450)
        self.side = 1

    def launch(self, x, y):
        if self.shoot_timer >= self.shoot_delay:
            if self.side == 1:
                AmmoRocket(x - 16, y, self.ammo)
                self.side = 2
            else:
                AmmoRocket(x + 16, y, self.ammo)
                self.side = 1
            self.shoot_timer = 0 

class WeaponThrower(WeaponBase):
    def __init__(self, ammo):
        WeaponBase.__init__(self, ammo)
        self.setFirerate(2000)

    def launch(self, x, y):
        if self.shoot_timer >= self.shoot_delay:
            AmmoFlame(x, y, self.ammo)
            self.shoot_timer = 0 


# Ammo types
feat_player_beam_default = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_BLUE_DEFAULT,
    "imageset_explosion": GR_AMMO_BLUE_EXPLOSION,
    "sound_launch": snd_laser,
    "sound_explosion": snd_small_explo,
    "speedy": -10.0,
    "energy": 10,  
}

feat_player_flame = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_FLAME,
    "imageset_explosion": GR_AMMO_FLAME_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_small_explo,
    "speedy": -10.0,
    "energy": 4,  
}

feat_player_rocket = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_ROCKET_DEFAULT,
    "imageset_explosion": GR_AMMO_ROCKET_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_small_explo,
    "speedy": -0.01,
    "energy": 12,  
}

feat_enemy_beam_default = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_PINK_DEFAULT,
    "imageset_explosion": GR_AMMO_PINK_EPXLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_laser_enemy,
    "speedy": 6.0,
    "energy": 2,  
}

# Enemy class
class NewEnemy(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, features["image_default"], enemy_group)
        self.hostile_group = player_ammo_group
        self.hor_margin = -24
        self.ver_margin = -24
        self.features = features
        self.setAnimation(self.imageset_default, 0)
        self.imageset_hilight = features["animation_blink"]
        self.type = features["type"]
        self.score = features["score"]
        self.hitpoints = features["hitpoints"]
        self.weapon = features["weapon"](features["ammo"])
        self.accuracy = 16
        self.rect = self.rect.move(x, y)
        self.alignHitBox(self.rect)
        self.speed = features["initial_speed"]
        self.killed = False

    # Passive movement & collision detection
    def update(self, level, offset, player):
        # Check if dead
        if self.destroyed() == True:
            self.explode(GR_EFFECT_EXPLOSION_BIG, snd_enemy_death)
            self.killed = True
            # Create coin
            Collectable(self.rect.centerx, self.rect.centery, GR_ACCESSORIES_COIN)
            Collectable(self.rect.centerx, self.rect.centery, GR_ACCESSORIES_COIN)

        # Check if outside area
        if self.outsideArea(level):
            self.kill()

        # Check collision ammo
        if self.collisionToEnemy():
            self.hitpoints -= 1
            self.setAnimation(self.imageset_hilight, 12)

        # Check collision to player
        if pygame.sprite.spritecollideany(self, player_group, self.collided):
            self.hitpoints = 0

        self.bounceFromWalls(level, offset)

        # Check shooting delay
        if abs(player.rect.centerx - self.rect.centerx) < self.accuracy:
            self.weapon.launch(self.rect.centerx, self.rect.bottom)

        # Update shooting delay
        self.weapon.shoot_timer += 1

        # Change animation frame
        self.changeFrame()

    def move(self, scroll_speed):
        # Keep on scrolling
        self.rect = self.rect.move(self.speed)
        self.rect = self.rect.move(0, scroll_speed)
        self.alignHitBox(self.rect)

def selectEnemy(x, y, character):
    if character == "X": 
        return NewEnemy(x, y, feat_enemy_fighter)
    elif character == "O":
        return NewEnemy(x, y, feat_enemy_spike)
    elif character == "Z":    
        return NewEnemy(x, y, feat_enemy_boss)

feat_enemy_fighter = {
    "type": "Ship",
    "image_default": GR_ENEMY_FIGHTER_DEFAULT,
    "animation_blink": GR_ENEMY_FIGHTER_BLINK,
    "weapon": WeaponDouble,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 2,
    "shoot_delay": 40,
    "initial_speed": (1.0, 0.0),
    "score": 10
}
feat_enemy_spike = {
    "type": "Spike",
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 2,
    "shoot_delay": 1000,
    "initial_speed": (-1.0, 0.0),
    "score": 5
} 
feat_enemy_boss = {
    "type": "Boss",
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponMinigun,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 15,
    "shoot_delay": 10,
    "initial_speed": (-1.0, 0.0),
    "score": 50
}


