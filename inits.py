import sys, pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) 

# Define displays
# Screen parameters
size = width, height = 1366, 768
player_start_x = round(width/2)
player_start_y = round(height-100)
#pygame.FULLSCREEN
#SCREEN = pygame.display.set_mode(size, FULLSCREEN | HWACCEL)  
SCREEN = pygame.display.set_mode(size)

# Global variables
framerate = 100
basic_scroll_speed = 2
offset = 0
current_level = 0 
score = 0
boss_alive = True

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
color_bg_default = BLACK
color_text = WHITE

def loadImages(image_list):
    folder = IMG_FOLDER
    i = 0
    while i < len(image_list):
        image_list[i] = pygame.image.load(folder + image_list[i]).convert_alpha()
        i += 1
    return image_list

def loadSound(filename, volume):
    folder = SND_FOLDER
    filename = folder + filename
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    return sound

def loadMusic(filename):
    folder = MUS_FOLDER
    filename = folder + filename
    sound = pygame.mixer.music.load(filename)
    return sound

# Asset folders for images and sounds
IMG_FOLDER = "assets/"
SND_FOLDER = "sounds/"
MUS_FOLDER = "music/"

#graphics
GR_APPICON = loadImages([
    "ship_default.png"])
GR_PLAYER_BODY_DEFAULT = loadImages([
    "ship_default.png"])
GR_PLAYER_BODY_BLINK = loadImages([
    "ship_hilight.png", 
    "ship_hilight.png", 
    "ship_hilight.png"])
GR_PLAYER_BODY_UP = loadImages([
    "ship_thrust1.png",
    "ship_thrust2.png"])
GR_ENEMY_FIGHTER_DEFAULT = loadImages([
    "enemy_default.png"])
GR_ENEMY_FIGHTER_BLINK = loadImages([
    "enemy_hilight.png", 
    "enemy_hilight.png", 
    "enemy_hilight.png"])
GR_ENEMY_SPIKE_DEFAULT = loadImages([
    "enemy_spike_default.png",
    "enemy_spike_default2.png"])
GR_ENEMY_SPIKE_BLINK = loadImages([
    "enemy_spike_hilight.png", 
    "enemy_spike_hilight.png", 
    "enemy_spike_hilight.png"])
GR_ENEMY_BIG_DEFAULT = loadImages(["enemy_big.png"])
GR_ENEMY_BIG_BLINK = loadImages([
    "enemy_big_hilight.png", 
    "enemy_big_hilight.png", 
    "enemy_big_hilight.png"])
GR_AMMO_BLUE_DEFAULT = loadImages(["ammo_blue.png"])
GR_AMMO_BLUE_EXPLOSION = loadImages([
    "exp_blue1.png", 
    "exp_blue2.png", 
    "exp_blue3.png", 
    "exp_blue4.png"])
GR_AMMO_PINK_DEFAULT = loadImages(["ammo_pink.png"])
GR_AMMO_PINK_EPXLOSION = loadImages([
    "exp_pink1.png", 
    "exp_pink2.png", 
    "exp_pink3.png", 
    "exp_pink4.png"])
GR_EFFECT_EXPLOSION_BIG = loadImages([
    "exp_round1.png", 
    "exp_round2.png", 
    "exp_round3.png", 
    "exp_round4.png", 
    "exp_round5.png", 
    "exp_round6.png"])
GR_UI_HEART_DEFAULT = loadImages(["heart.png"])

# Load level image sets
GR_WALLSET_STONE = loadImages([
    "wall_middle.png",
    "wall_single.png",
    "bar_vertical.png",
    "bar_horizontal.png",
    "point_up.png",
    "point_down.png",
    "point_left.png",
    "point_right.png",
    "wall_top.png",
    "wall_bottom.png",
    "wall_left.png",
    "wall_right.png",
    "corner_top_left.png",
    "corner_top_right.png",
    "corner_bottom_right.png",
    "corner_bottom_left.png"])
    
GR_WALLSET_TECH = loadImages([
    "tech_wall_middle.png",
    "tech_wall_single.png",
    "tech_bar_vertical.png",
    "tech_bar_horizontal.png",
    "tech_point_up.png",
    "tech_point_down.png",
    "tech_point_left.png",
    "tech_point_right.png",
    "tech_wall_top.png",
    "tech_wall_bottom.png",
    "tech_wall_left.png",
    "tech_wall_right.png",
    "tech_corner_top_left.png",
    "tech_corner_top_right.png",
    "tech_corner_bottom_right.png",
    "tech_corner_bottom_left.png"])

# Load sounds
snd_laser = loadSound("laser1.ogg", 0.15)
snd_laser_enemy = loadSound("laser2.ogg", 0.3)
snd_player_death = loadSound("defeated.ogg", 0.8)
snd_enemy_death = loadSound("hit1.ogg", 0.8)
snd_small_explo = loadSound("hit3.ogg", 0.3)

# Load music
music = loadMusic("Starmusic_02.mp3")

# Enemy feature dictionaries

enemy_types_list = [
    {
        "type": "Ship",
        "character": "X", 
        "image_default": GR_ENEMY_FIGHTER_DEFAULT,
        "animation_blink": GR_ENEMY_FIGHTER_BLINK,
        "hit_points": 2,
        "shoot_delay": 40,
        "initial_speed": (1, 0),
        "score": 10
    },
    {
        "type": "Spike",
        "character": "O",
        "image_default": GR_ENEMY_SPIKE_DEFAULT,
        "animation_blink": GR_ENEMY_SPIKE_BLINK,
        "hit_points": 2,
        "shoot_delay": 1000,
        "initial_speed": (-1, 0),
        "score": 5
    },
    {
        "type": "Boss",
        "character": "Z",
        "image_default": GR_ENEMY_BIG_DEFAULT,
        "animation_blink": GR_ENEMY_BIG_BLINK,
        "hit_points": 15,
        "shoot_delay": 10,
        "initial_speed": (-1, 0),
        "score": 50
    }
]