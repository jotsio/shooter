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
        self.level = features["level"]

    def createCollectables(self, bonus):
        value = random.randint(0, 3) + random.randint(0, 3) + random.randint(0, 3) + bonus
        table = collectables_list
        if value >= len(table) - 1:
            value = len(table) -1
        Collectable(self.rect.centerx, self.rect.centery, table[value])

    # Passive movement & collision detection
    def update(self, level, offset, player):
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

        # Bounces form walls
        self.bounceFromRect(level.locateCollision(self.hitbox, offset))

        self.bounceFromSides(level, offset)

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
    "level": 2,
    "image_default": GR_ENEMY_FIGHTER_DEFAULT,
    "animation_blink": GR_ENEMY_FIGHTER_BLINK,
    "weapon": WeaponDouble,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 40,
    "initial_speed": (1.0, 0.0),
    "score": 10
}

feat_enemy_spike = {
    "type": "Spike",
    "level": 2,
    "image_default": GR_ENEMY_SPIKE_DEFAULT,
    "animation_blink": GR_ENEMY_SPIKE_BLINK,
    "weapon": WeaponSingle,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 10,
    "shoot_delay": 1000,
    "initial_speed": (-1.0, 0.0),
    "score": 5
} 

feat_enemy_boss = {
    "type": "Boss",
    "level": 10,
    "image_default": GR_ENEMY_BIG_DEFAULT,
    "animation_blink": GR_ENEMY_BIG_BLINK,
    "weapon": WeaponMinigun,
    "ammo": feat_enemy_beam_default,
    "hitpoints": 120,
    "shoot_delay": 10,
    "initial_speed": (-1.0, 0.0),
    "score": 50
}

