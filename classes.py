import pygame
from pygame.locals import *
#from inits import *

# Create groups
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
player_ammo_group = pygame.sprite.Group()
enemy_ammo_group = pygame.sprite.Group()
effects_group = pygame.sprite.Group()

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