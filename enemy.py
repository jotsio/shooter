import math
import random
from inits import *
from classes import *
from weapons import *
from collectables import *

# Enemy class
class NewEnemy(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, features):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, features["image_default"], enemy_group)
        self.features = features
        self.id = random.randint(1,1000)
        self.hostile_group = player_ammo_group
        self.hor_margin = -24
        self.ver_margin = -24
        self.orientation = features["orientation"]
        self.features = features
        self.setAnimation(self.imageset_default, 0)
        self.imageset_hilight = features["animation_blink"]
        self.type = features["type"]
        self.score = features["score"]
        self.hitpoints = features["hitpoints"]
        self.weapon = features["weapon"](features["ammo"], self.orientation)
        self.accuracy = 16
        self.rect = self.rect.move(x, y)
        self.alignHitBox(self.rect)
        self.speed = features["initial_speed"]
        self.level = features["level"]
        

    def createCollectables(self, bonus):
        value = random.randint(0, 3) + random.randint(0, 4) + random.randint(0, 3) + bonus
        table = collectables_list
        if value >= len(table) - 1:
            value = len(table) -1
        Collectable(self.rect.centerx, self.rect.centery, table[value])

    # Passive movement & collision detection
    def update(self, level, offset, player, scroll_speed):
        # Check if dead
        if self.destroyed() == True:
            self.explode(GR_EFFECT_EXPLOSION_BIG, snd_enemy_death)
            self.killed = True
            # Create collectables
            self.createCollectables(self.level)

        # Check if outside area
        if self.outsideArea(level):
            self.kill()

        # Check collision to ammo
        damage = self.getCollisionDamage(self.hostile_group)
        if damage:
            self.hitpoints -= damage
            self.setAnimation(self.imageset_hilight, 12)

        # Check collision to player
        if pygame.sprite.spritecollideany(self, player_group, self.collided):
            self.hitpoints = 0

        # Bounces from walls
        self.bounceFromRect(level.locateCollision(self.hitbox, offset))
        self.bounceFromSides(level, offset)

        # Shoot if player on shooting line
        distance_x = self.rect.centerx - player.rect.centerx
        distance_y = self.rect.centery - player.rect.centery 
        distance_y = distance_y + scroll_speed * distance_x / self.features["ammo"]["speed"]

        offset_x = self.orientation[0] * self.rect.width / 3
        offset_y = self.orientation[1] * self.rect.height / 3       
        if self.orientation[0] * distance_x <= 0 and self.orientation[1] * distance_y <= 0:
            if (self.orientation[0] == 0 and abs(distance_x) <= self.accuracy) or (self.orientation[1] == 0 and abs(distance_y) <= self.accuracy):
                self.weapon.launch(self.rect.centerx + offset_x, self.rect.centery + offset_y)
            if (self.orientation[0] != 0 and self.orientation[1] != 0) and (abs(abs(distance_x) - abs(distance_y)) <= self.accuracy):
                self.weapon.launch(self.rect.centerx + offset_x, self.rect.centery + offset_y)

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
    elif character == "Y":    
        return NewEnemy(x, y, feat_enemy_turret_left)
    elif character == "U":    
        return NewEnemy(x, y, feat_enemy_turret_right)

feat_enemy_turret_left = {
    "type": "Turret",
    "level": 0,
    "image_default": GR_ENEMY_TURRET_DEFAULT,
    "animation_blink": GR_ENEMY_TURRET_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 8,
    "shoot_delay": 20,
    "initial_speed": (0.0, 0.0),
    "score": 5,
    "orientation": (-1.0, 1.0)
}

feat_enemy_turret_right = {
    "type": "Turret",
    "level": 0,
    "image_default": GR_ENEMY_TURRET_DEFAULT,
    "animation_blink": GR_ENEMY_TURRET_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 8,
    "shoot_delay": 20,
    "initial_speed": (0.0, 0.0),
    "score": 5,
    "orientation": (1.0, 1.0)
}

feat_enemy_fighter = {
    "type": "Ship",
    "level": 10,
    "image_default": GR_ENEMY_FIGHTER_DEFAULT,
    "animation_blink": GR_ENEMY_FIGHTER_BLINK,
    "weapon": WeaponDouble,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 40,
    "initial_speed": (1.0, 0.0),
    "score": 10,
    "orientation": (0.0, 1.0)
}

feat_enemy_spike = {
    "type": "Spike",
    "level": 5,
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 1000,
    "initial_speed": (-1.0, 0.0),
    "score": 5,
    "orientation": (-1.0, 0.0)
} 

feat_enemy_boss = {
    "type": "Boss",
    "level": 20,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponMinigun,
    "ammo": feat_enemy_missile,
    "hitpoints": 120,
    "shoot_delay": 4,
    "initial_speed": (-1.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0)
}

