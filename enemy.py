import math
import random
from inits import *
from assets import *
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
        self.collectables_list = features["collectables"]
        self.setAnimation(self.imageset_default, 0)
        self.imageset_hilight = features["animation_blink"]
        self.type = features["type"]
        self.score = features["score"]
        self.hitpoints = features["hitpoints"]
        self.weapon = features["weapon"](self, features["ammo"], self.orientation)
        self.accuracy = features["accuracy"]
        self.alignHitBox(self.rect)
        self.speed = features["initial_speed"]
        self.level = features["level"]
        
    def createCollectables(self, c_list):
        value = random.randint(0, (len(c_list) - 1))
        Collectable(self.rect.centerx, self.rect.centery, c_list[value])

    # Passive movement & collision detection
    def update(self, level, offset, player, scroll_speed):
        # Check if dead
        if self.destroyed() == True:
            self.explode(GR_EFFECT_EXPLOSION_BIG, snd_enemy_death)
            self.killed = True
            # Create collectables
            self.createCollectables(self.collectables_list)

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
            if self.type != "Boss":
                self.hitpoints = 0

        # Bounces from walls
        self.bounceFromRect(level.locateCollision(self.hitbox, offset))
        self.bounceFromSides(level, offset)

        # Shoot if player on shooting line
        distance_x = self.rect.centerx - player.rect.centerx
        distance_y = self.rect.centery - player.rect.centery 
        distance_y = distance_y + scroll_speed * abs(distance_x) / self.features["ammo"]["speed"]

        offset_x = self.orientation[0] * self.rect.width / 3
        offset_y = self.orientation[1] * self.rect.height / 3       
        if self.orientation[0] * distance_x <= 0 and self.orientation[1] * distance_y <= 0:
            if (self.orientation[0] == 0 and abs(distance_x) <= self.accuracy) or (self.orientation[1] == 0 and abs(distance_y) <= self.accuracy):
                self.weapon.launch(self.rect.centerx + offset_x, self.rect.centery + offset_y, level, offset)
            if (self.orientation[0] != 0 and self.orientation[1] != 0) and (abs(abs(distance_x) - abs(distance_y)) <= self.accuracy):
                self.weapon.launch(self.rect.centerx + offset_x, self.rect.centery + offset_y, level, offset)

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
        return NewEnemy(x, y, feat_enemy_fighter_double)
    if character == "V": 
        return NewEnemy(x, y, feat_enemy_fighter_single)
    elif character == "O":
        return NewEnemy(x, y, feat_enemy_spike_down)
    elif character == ">":
        return NewEnemy(x, y, feat_enemy_spike_right)      
    elif character == "<":
        return NewEnemy(x, y, feat_enemy_spike_left)    
    elif character == "Y":    
        return NewEnemy(x, y, feat_enemy_turret_down)
    elif character == "L":    
        return NewEnemy(x, y, feat_enemy_turret_right)
    elif character == "J":    
        return NewEnemy(x, y, feat_enemy_turret_left)
    elif character == "Z":    
        return NewEnemy(x, y, feat_enemy_boss)
    elif character == "F":    
        return NewEnemy(x, y, feat_enemy_boss_flame)
    elif character == "M":    
        return NewEnemy(x, y, feat_enemy_boss_missile)
    elif character == "R":    
        return NewEnemy(x, y, feat_enemy_boss_rocket)
    elif character == "D":    
        return NewEnemy(x, y, feat_enemy_boss_distributor)

feat_enemy_turret_left = {
    "type": "Turret",
    "level": 0,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_TURRETLEFT_DEFAULT,
    "animation_blink": GR_ENEMY_TURRETLEFT_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 8,
    "shoot_delay": 16,
    "initial_speed": (0.0, 0.0),
    "score": 5,
    "orientation": (-1.0, 1.0),
    "accuracy": 16
}

feat_enemy_turret_right = {
    "type": "Turret",
    "level": 0,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_TURRETRIGHT_DEFAULT,
    "animation_blink": GR_ENEMY_TURRETRIGHT_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 8,
    "shoot_delay": 16,
    "initial_speed": (0.0, 0.0),
    "score": 5,
    "orientation": (1.0, 1.0),
    "accuracy": 16
}

feat_enemy_turret_down = {
    "type": "Turret",
    "level": 0,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_TURRET_DEFAULT,
    "animation_blink": GR_ENEMY_TURRET_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 8,
    "shoot_delay": 16,
    "initial_speed": (0.0, 0.0),
    "score": 5,
    "orientation": (0.0, 1.0),
    "accuracy": 16
}

feat_enemy_fighter_single = {
    "type": "Ship",
    "level": 10,
    "collectables": collectables_list_medium,
    "image_default": GR_ENEMY_FIGHTER_DEFAULT,
    "animation_blink": GR_ENEMY_FIGHTER_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 30,
    "initial_speed": (1.0, 0.0),
    "score": 10,
    "orientation": (0.0, 1.0),
    "accuracy": 16
}

feat_enemy_fighter_double = {
    "type": "Ship",
    "level": 15,
    "collectables": collectables_list_medium,
    "image_default": GR_ENEMY_FIGHTER_DEFAULT,
    "animation_blink": GR_ENEMY_FIGHTER_BLINK,
    "weapon": WeaponDouble,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 40,
    "initial_speed": (1.0, 0.0),
    "score": 10,
    "orientation": (0.0, 1.0),
    "accuracy": 24
}

feat_enemy_spike_down = {
    "type": "Spike",
    "level": 5,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 60,
    "initial_speed": (-1.0, 0.0),
    "score": 5,
    "orientation": (0.0, 1.0),
    "accuracy": 16
} 

feat_enemy_spike_left = {
    "type": "Spike",
    "level": 5,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 60,
    "initial_speed": (-1.0, 0.0),
    "score": 5,
    "orientation": (-1.0, 0.0),
    "accuracy": 16
} 

feat_enemy_spike_right = {
    "type": "Spike",
    "level": 5,
    "collectables": collectables_list_small,
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 60,
    "initial_speed": (-1.0, 0.0),
    "score": 5,
    "orientation": (1.0, 0.0),
    "accuracy": 16
} 

feat_enemy_boss = {
    "type": "Boss",
    "level": 20,
    "collectables": collectables_list_boss,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponMinigun,
    "ammo": feat_enemy_beam_large,
    "hitpoints": 120,
    "shoot_delay": 30,
    "initial_speed": (-1.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0),
    "accuracy": 16
}

feat_enemy_boss_flame = {
    "type": "Boss",
    "level": 20,
    "collectables": collectables_list_boss,
    "image_default": GR_ENEMY_BIGFLAME_DEFAULT,
    "animation_blink": GR_ENEMY_BIGFLAME_BLINK,
    "weapon": WeaponBossThrower,
    "ammo": feat_enemy_flame,
    "hitpoints": 120,
    "shoot_delay": 2,
    "initial_speed": (-1.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0),
    "accuracy": 64
}

feat_enemy_boss_missile = {
    "type": "Boss",
    "level": 20,
    "collectables": collectables_list_boss,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponMissileLauncher,
    "ammo": feat_enemy_missile,
    "hitpoints": 120,
    "shoot_delay": 2,
    "initial_speed": (-1.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0),
    "accuracy": 256
}

feat_enemy_boss_rocket = {
    "type": "Boss",
    "level": 20,
    "collectables": collectables_list_boss,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponEnemyRocketLauncher,
    "ammo": feat_enemy_rocket,
    "hitpoints": 120,
    "shoot_delay": 2,
    "initial_speed": (-1.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0),
    "accuracy": 32
}

feat_enemy_boss_distributor = {
    "type": "Boss",
    "level": 20,
    "collectables": collectables_list_boss,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponDistributor,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 120,
    "shoot_delay": 1,
    "initial_speed": (2.0, 0.0),
    "score": 50,
    "orientation": (0.0, 1.0),
    "accuracy": 512
}