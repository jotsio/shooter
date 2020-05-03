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

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
color_bg_default = BLACK
color_text = WHITE

def loadImageSet(image_list):
    folder = IMG_FOLDER
    i = 0
    while i < len(image_list):
        image_list[i] = pygame.image.load(folder + image_list[i]).convert_alpha()
        i += 1
    return image_list

def loadImage(filename):
    folder = IMG_FOLDER
    filename = folder + filename
    image = pygame.image.load(filename).convert_alpha()
    return image

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
GR_MYSHIP = loadImage("ship_default.png")
GR_ENEMYSHIP = loadImage("enemy_default.png")
GR_AMMO = loadImage("ammo_blue.png")
GR_AMMO_ENEMY = loadImage("ammo_pink.png")
GR_HEART = loadImage("heart.png")

# Load animations
ANIM_MYSHIP_BLINK = loadImageSet([
    "ship_hilight.png", 
    "ship_hilight.png", 
    "ship_hilight.png"])

ANIM_ENEMYSHIP_BLINK = loadImageSet([
    "enemy_hilight.png", 
    "enemy_hilight.png", 
    "enemy_hilight.png"])

ANIM_BLUEEXP = loadImageSet([
    "exp_blue1.png", 
    "exp_blue2.png", 
    "exp_blue3.png", 
    "exp_blue4.png"])

ANIM_PINKEXP = loadImageSet([
    "exp_pink1.png", 
    "exp_pink2.png", 
    "exp_pink3.png", 
    "exp_pink4.png"])

ANIM_ORANGEEXP = loadImageSet([
    "exp_round1.png", 
    "exp_round2.png", 
    "exp_round3.png", 
    "exp_round4.png", 
    "exp_round5.png", 
    "exp_round6.png"])

# Load level image sets
wallset_stone = loadImageSet([
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
    
wallset_tech = loadImageSet([
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
