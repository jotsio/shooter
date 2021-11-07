import pygame
from pygame.locals import *
import random

size = width, height = 1366, 768

player_start_x = round(width/2)
player_start_y = round(height-100)
update_offset_up = -2560
update_offset_down = 256

# Global variables
framerate = 60
basic_scroll_speed = 2

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
DARK_RED = 64, 0, 0
GRAY_800 = 32, 32, 32
VIOLET_800 = 26, 0, 62
VIOLET_700 = 40, 20, 80

color_bg_stars_default = BLACK
color_bg_stars_hilight = GRAY_800
color_bg_clouds_default = VIOLET_800
color_bg_clouds_hilight = VIOLET_700

color_text = WHITE

# Screen
SCREEN = pygame.display.set_mode(size, FULLSCREEN | HWACCEL, SCALED)  
pygame.display.Info()
#SCREEN = pygame.display.set_mode(size, FULLSCREEN, SCALED)

# Sound
pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=512, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) 
pygame.init()

# Random list for maps
random.seed(1)
randomlist = []
for x in range(100):
    randomlist.append(random.randint(1,15))
