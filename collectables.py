import math
import random
from inits import *
from classes import *


class Collectable(pygame.sprite.Sprite, Base):
    def __init__(self, x, y, imageset, boost):
        pygame.sprite.Sprite.__init__(self)
        Base.__init__(self, x, y, imageset, effects_group)
        self.hostile_group = player_group
        self.boost = boost
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
        self.score = 1
    
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
