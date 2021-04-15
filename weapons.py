import math
import random
from inits import *
from classes import *


# Basic Ammunition
class AmmoBasic(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, direction, features):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, features["imageset_default"], features["own_group"])
        self.hostile_group = features["enemy_group"]
        self.features = features
        # Centrify position
        self.rect = self.rect.move(round(-self.rect.w / 2), round(-self.rect.h / 2))
        self.alignHitBox(self.rect)
        # Vertical speed
        self.speed = direction
        self.speed = (self.speed[0] * features["speed"], self.speed[1] * features["speed"])
        self.hit_energy = features["energy"]
        if self.hit_energy > 100:
            self.destroys_walls = True
        features["sound_launch"].play()


    def basicAmmoChecks(self, level, offset, player):
        # Explode if collided to level walls
        hitted_block = level.checkCollision(self.hitbox, offset)
        if hitted_block != None:
            if self.destroys_walls:
                self.destroyWall(level, hitted_block[0], hitted_block[1], hitted_block[2])
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

    def update(self, level, offset, player):
        self.basicAmmoChecks(level, offset, player)

    def explode(self, animation, sound):
        NewEffect(self.rect.centerx, self.rect.centery, animation)
        sound.play()

# Beam
class AmmoLaser(AmmoBasic):
    def __init__(self, x, y, direction, features, level, offset):
        AmmoBasic.__init__(self, x, y, direction, features)
        self.scaleBeamByHit(level, offset, x, y)
        

    def scaleBeamByHit(self, level, offset, x, y):
        y_hit = 0
        while self.rect.y > -64:
            hitted_block = level.checkCollision(self.rect, offset)
            hitted_enemy = self.collisionToEnemy()
            if hitted_block != None or hitted_enemy != None:
                y_hit = self.rect[1]
                self.explode(self.features["imageset_explosion"], self.features["sound_explosion"])
                if hitted_block:
                    self.destroyWall(level, hitted_block[0], hitted_block[1], hitted_block[2])
                break
            self.rect = self.rect.move(0, -8)
            self.alignHitBox(self.rect)
        beam_height = y - y_hit
        self.image = pygame.transform.scale(self.animation[0], (self.rect.width, beam_height))
        self.rect = pygame.Rect(x - self.rect.w / 2, y_hit, self.rect.width, beam_height)


    def update(self, level, offset, player):
        player.beam = True
        self.scaleBeamByHit(level, offset, player.rect.centerx, player.rect.centery)
        if player.fire == False:    
            self.kill()
            player.beam = False
        self.counter += 1

    def explode(self, animation, sound):
        NewEffect(self.rect.centerx, self.rect.y, animation)
        sound.play()

class AmmoMissile(AmmoBasic):
    def update(self, level, offset, player):
        self.basicAmmoChecks(level, offset, player)

        # Guides itself towards player
        if self.rect.centerx > player.rect.centerx:
            self.speed = (self.speed[0] - 0.1, self.speed[1])
        if self.rect.centerx < player.rect.centerx:
            self.speed = (self.speed[0] + 0.1, self.speed[1])

    def move(self, scroll_speed):
        self.rect = self.rect.move(self.speed)
        self.rect = self.rect.move(0, scroll_speed)
        self.alignHitBox(self.rect)
        sy = self.speed[1]
        if sy < 10.0:    
            sy += 0.1
        else:
            sy = 10.0
        self.speed = (self.speed[0], sy) 

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
    def update(self, level, offset, player):
        self.basicAmmoChecks(level, offset, player)
        
        if self.counter >= len(self.animation) * self.ticks_in_frame:
            self.kill()

        self.applyFriction(0.0, 0.2)

# Weapons
class WeaponBase():
    def __init__(self, ammo, orientation):
        self.ammo = ammo
        self.shoot_delay = 0
        self.power = 1.0
        self.shoot_timer = 0
        self.magazine = 0
        self.orientation = orientation
    
    def setFirerate(self, rpm):
        self.shoot_delay = round(100 * 60 / rpm)

    def releaseTrigger(self):
        self.shoot_timer = 0

class WeaponSingle(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(500)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponDouble(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(500)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x - 16, y, self.orientation, self.ammo)
            AmmoBasic(x + 16, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponMinigun(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(1000)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponLaser(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(500)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoLaser(x, y, self.orientation, self.ammo, level, offset)
            self.shoot_timer = 0 
            self.magazine -= 1
        
class WeaponLauncher(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(500)
        self.side = 1

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            if self.side == 1:
                AmmoRocket(x - 16, y, self.orientation, self.ammo)
                self.side = 2
            else:
                AmmoRocket(x + 16, y, self.orientation, self.ammo)
                self.side = 1
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponThrower(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(2000)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoFlame(x, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponBossThrower(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(2000)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoFlame(x - 58, y, self.orientation, self.ammo)
            AmmoFlame(x + 58, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponMissileLauncher(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(100)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoMissile(x, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponEnemyRocketLauncher(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(100)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, self.orientation, self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

class WeaponDistributor(WeaponBase):
    def __init__(self, host, ammo, orientation):
        WeaponBase.__init__(self, ammo, orientation)
        self.setFirerate(300)

    def launch(self, x, y, level, offset):
        if self.shoot_timer >= self.shoot_delay:
            AmmoBasic(x, y, (0, 1), self.ammo)
            AmmoBasic(x, y, (0.5,1), self.ammo)
            AmmoBasic(x, y, (-0.5,1), self.ammo)
            self.shoot_timer = 0 
            self.magazine -= 1

# Ammo types
feat_player_beam_default = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_BLUE_DEFAULT,
    "imageset_explosion": GR_AMMO_BLUE_EXPLOSION,
    "sound_launch": snd_laser,
    "sound_explosion": snd_small_explo,
    "speed": 10.0,
    "energy": 8,  
}

feat_player_beam_minigun = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_BLUE_DEFAULT,
    "imageset_explosion": GR_AMMO_BLUE_EXPLOSION,
    "sound_launch": snd_laser_minigun,
    "sound_explosion": snd_small_explo,
    "speed": 10.0,
    "energy": 3,  
}

feat_player_flame = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_FLAME,
    "imageset_explosion": GR_AMMO_FLAME_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_medium_explo,
    "speed": 10.0,
    "energy": 3,  
}

feat_player_laser = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_BLUE_LASER,
    "imageset_explosion": GR_AMMO_BLUE_LASER_HIT,
    "sound_launch": snd_laser,
    "sound_explosion": snd_small_explo,
    "speed": 0.0,
    "energy": 4,  
}

feat_enemy_flame = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_FLAME,
    "imageset_explosion": GR_AMMO_FLAME_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_medium_explo,
    "speed": 10.0,
    "energy": 1,  
}

feat_player_rocket = {
    "own_group": player_ammo_group,
    "enemy_group": enemy_group,
    "imageset_default": GR_AMMO_ROCKET_DEFAULT,
    "imageset_explosion": GR_AMMO_ROCKET_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_medium_explo,
    "speed": 0.01,
    "energy": 11,  
}

feat_enemy_beam_default = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_PINK_DEFAULT,
    "imageset_explosion": GR_AMMO_PINK_EXPLOSION,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_medium_explo,
    "speed": 5.0,
    "energy": 1,  
}

feat_enemy_beam_large = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_PINKBIG_DEFAULT,
    "imageset_explosion": GR_EFFECT_EXPLOSION_PINK_LARGE,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_medium_explo,
    "speed": 8.0,
    "energy": 1,  
}

feat_enemy_missile = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_MISSILE_DEFAULT,
    "imageset_explosion": GR_AMMO_PINK_EXPLOSION_BIG,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_wall_destroy,
    "speed": 2.0,
    "energy": 101,  
}

feat_enemy_rocket = {
    "own_group": enemy_ammo_group,
    "enemy_group": player_group,
    "imageset_default": GR_AMMO_ROCKET_PINK,
    "imageset_explosion": GR_AMMO_PINK_EXPLOSION_BIG,
    "sound_launch": snd_laser_enemy,
    "sound_explosion": snd_wall_destroy,
    "speed": 2.0,
    "energy": 101,  
}