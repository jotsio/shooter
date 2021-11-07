import math
import random
from inits import *
from assets import *
from classes import *


class Collectable(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, features["imageset"], effects_group)
        self.hostile_group = player_group
        self.type = features["type"]
        self.boost = features["boost"]
        # Centrify position
        self.rect = self.rect.move(round(-self.rect.w / 2), round(-self.rect.h / 2))
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
            self.killed = True
            snd_coin.play()
        
        # Bounce from walls
        self.bounceFromRect(level.locateCollision(self.hitbox, offset))

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


c_coin = {
    "type": "money",
    "imageset": GR_ACCESSORIES_COIN,
    "boost": 0
    }

c_weapon_single = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_SINGLE,
    "boost": 1
    }

c_weapon_double = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_DOUBLE,
    "boost": 2
    }

c_weapon_minigun = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_MINIGUN,
    "boost": 3
    }

c_weapon_launcher = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_LAUNCHER,
    "boost": 4
    }

c_weapon_thrower = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_THROWER,
    "boost": 5
    }

c_weapon_laser = {
    "type": "weapon",
    "imageset": GR_ACCESSORIES_WEAPON_LASER,
    "boost": 6
    }

c_powerup = {
    "type": "powerup",
    "imageset": GR_ACCESSORIES_POWERUP,
    "boost": 0
    }

c_shield = {
    "type": "shield",
    "imageset": GR_ACCESSORIES_SHIELD,
    "boost": 0
    }

collectables_list_small = [
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_shield,
    c_powerup
]

collectables_list_medium = [
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_coin,
    c_weapon_double,
    c_weapon_minigun,
    c_shield,
    c_powerup
]

collectables_list_boss = [
    c_weapon_minigun,
    c_weapon_launcher,
    c_weapon_thrower,
    c_weapon_laser,
    c_powerup,
    c_powerup,
]

