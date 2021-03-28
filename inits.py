import sys, pygame
from pygame.locals import *
import random

pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=512, allowedchanges=AUDIO_ALLOW_FREQUENCY_CHANGE | AUDIO_ALLOW_CHANNELS_CHANGE) 
pygame.init()

# Define displays
# Screen parameters
size = width, height = 1366, 768
player_start_x = round(width/2)
player_start_y = round(height-100)
update_offset_up = -2560
update_offset_down = 256

# Font
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None,32)
font_large = pygame.font.Font(None,48)

# Text positions
textplace_center = (width // 2, height // 2)
textplace_rightdown_first = (width - 64, height - 64)
textplace_rightdown_second = (width - 128, height - 64)

#pygame.FULLSCREEN
#SCREEN = pygame.display.set_mode(size, FULLSCREEN | HWACCEL)  
SCREEN = pygame.display.set_mode(size, FULLSCREEN)

# Global variables
framerate = 50
basic_scroll_speed = 2
offset = 0
current_level = 0 
score = 0
money = 0

# Random list for maps
random.seed(1)
randomlist = []
for x in range(100):
    randomlist.append(random.randint(1,15))

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

def loadImages(image_list):
    folder = IMG_FOLDER
    i = 0
    while i < len(image_list):
        image_list[i] = pygame.image.load(folder + image_list[i]).convert_alpha()
        i += 1
    return image_list

def loadTileset(subfolder):
    folder = TILES_FOLDER + subfolder
    filenames = TILES_LIST
    i = 0
    image_list = []
    while i < len(filenames):
        image_list.append(pygame.image.load(folder + filenames[i]).convert_alpha())
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
TILES_FOLDER = "tilesets/"
SND_FOLDER = "sounds/"
MUS_FOLDER = "music/"

# Tileset file names in right order
TILES_LIST = [
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
    "corner_bottom_left.png",
    "sec_wall_middle.png",
    "sec_wall_single.png",
    "sec_bar_vertical.png",
    "sec_bar_horizontal.png",
    "sec_point_up.png",
    "sec_point_down.png",
    "sec_point_left.png",
    "sec_point_right.png",
    "sec_wall_top.png",
    "sec_wall_bottom.png",
    "sec_wall_left.png",
    "sec_wall_right.png",
    "sec_corner_top_left.png",
    "sec_corner_top_right.png",
    "sec_corner_bottom_right.png",
    "sec_corner_bottom_left.png"]

# Load level image sets
GR_WALLSET_STONE = loadTileset("stone/")
GR_WALLSET_TECH = loadTileset("tech/")
GR_WALLSET_TOR = loadTileset("tor/")

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
GR_PLAYER_SHIELD = loadImages([
    "ship_shield_1.png",
    "ship_shield_2.png",
    "ship_shield_3.png",
    "ship_shield_4.png"])
GR_PLAYER_SHIELD_BLINK = loadImages([
    "ship_shield_1.png",
    "ship_shield_2.png",
    "ship_shield_3.png",
    "ship_shield_4.png",
    "ship_shield_1.png",
    "ship_shield_2.png",
    "ship_shield_3.png",
    "ship_shield_4.png",
    "transparent.png",
    "transparent.png",
    "transparent.png",
    "transparent.png",
    "transparent.png",
    "transparent.png",
    "transparent.png",
    "transparent.png"])
GR_PLAYER_SHADOW = loadImages([
    "ship_shadow.png"])
GR_ENEMY_TURRET_DEFAULT = loadImages([
    "enemy_turret_default.png"])
GR_ENEMY_TURRET_BLINK = loadImages([
    "enemy_turret_hilight.png",
    "enemy_turret_hilight.png",
    "enemy_turret_hilight.png"])
GR_ENEMY_TURRETLEFT_DEFAULT = loadImages([
    "enemy_turret_left.png"])
GR_ENEMY_TURRETLEFT_BLINK = loadImages([
    "enemy_turret_left_hilight.png",
    "enemy_turret_left_hilight.png",
    "enemy_turret_left_hilight.png"])
GR_ENEMY_TURRETRIGHT_DEFAULT = loadImages([
    "enemy_turret_right.png"])
GR_ENEMY_TURRETRIGHT_BLINK = loadImages([
    "enemy_turret_right_hilight.png",
    "enemy_turret_right_hilight.png",
    "enemy_turret_right_hilight.png"])
GR_ENEMY_FIGHTER_DEFAULT = loadImages([
    "enemy_default.png",
    "enemy_default2.png",
    "enemy_default3.png",
    "enemy_default2.png"])
GR_ENEMY_FIGHTER_BLINK = loadImages([
    "enemy_hilight.png", 
    "enemy_hilight.png", 
    "enemy_hilight.png"])
GR_ENEMY_SPIKE_DEFAULT = loadImages([
    "enemy_spike_default.png",
    "enemy_spike_default2.png",
    "enemy_spike_default3.png",
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
GR_ENEMY_BIGFLAME_DEFAULT = loadImages(["enemy_big_flame.png"])
GR_ENEMY_BIGFLAME_BLINK = loadImages([
    "enemy_big_flame_hilight.png", 
    "enemy_big_flame_hilight.png", 
    "enemy_big_flame_hilight.png"])
GR_AMMO_BLUE_DEFAULT = loadImages(["ammo_blue.png"])
GR_AMMO_BLUE_ROUND = loadImages(["ammo_blue_round.png"])
GR_AMMO_BLUE_EXPLOSION = loadImages([
    "exp_blue1.png", 
    "exp_blue2.png", 
    "exp_blue3.png", 
    "exp_blue4.png"])
GR_AMMO_ROCKET_EXPLOSION = loadImages([
    "exp_blue_large_1.png", 
    "exp_blue_large_2.png", 
    "exp_blue_large_3.png", 
    "exp_blue_large_4.png", 
    "exp_blue_large_5.png"])
GR_AMMO_ROCKET_DEFAULT = loadImages(["ammo_rocket.png"])
GR_AMMO_ROCKET_PINK = loadImages(["ammo_rocket_pink.png"])
GR_AMMO_MISSILE_DEFAULT = loadImages([
    "ammo_missile_1.png",
    "ammo_missile_2.png"])
GR_AMMO_FLAME = loadImages([
    "ammo_flame_1.png", 
    "ammo_flame_2.png",
    "ammo_flame_3.png",
    "ammo_flame_4.png",
    "ammo_flame_5.png",
    "ammo_flame_6.png",
    "ammo_flame_7.png",
    "ammo_flame_8.png",
    "ammo_flame_9.png",
    "ammo_flame_10.png"
    ])
GR_AMMO_FLAME_EXPLOSION = loadImages([
    "exp_flame_1.png", 
    "exp_flame_2.png",
    "exp_flame_3.png"
    ])
GR_AMMO_PINK_DEFAULT = loadImages(["ammo_pink.png"])
GR_AMMO_PINK_ROUND = loadImages(["ammo_pink_round.png"])
GR_AMMO_PINKBIG_DEFAULT = loadImages([
    "ammo_pink_big.png",
    "ammo_pink_big2.png",
    "ammo_pink_big3.png",
    "ammo_pink_big4.png"])
GR_AMMO_PINK_EXPLOSION = loadImages([
    "exp_pink1.png", 
    "exp_pink2.png", 
    "exp_pink3.png", 
    "exp_pink4.png"])

GR_AMMO_PINK_EXPLOSION_BIG = loadImages([
    "exp_pink_huge_1.png", 
    "exp_pink_huge_2.png", 
    "exp_pink_huge_3.png",
    "exp_pink_huge_4.png", 
    "exp_pink_huge_5.png"])

GR_EFFECT_EXPLOSION_PINK_LARGE = loadImages([
    "exp_pink_large_1.png", 
    "exp_pink_large_2.png", 
    "exp_pink_large_3.png",
    "exp_pink_large_4.png",
    "exp_pink_large_5.png"])

GR_EFFECT_EXPLOSION_BIG = loadImages([
    "exp_round1.png", 
    "exp_round2.png", 
    "exp_round3.png", 
    "exp_round4.png", 
    "exp_round5.png", 
    "exp_round6.png"])
GR_UI_HEART_DEFAULT = loadImages(["heart.png"])
GR_ACCESSORIES_WEAPON_SINGLE = loadImages([
    "accessory_weapon_single.png"])
GR_ACCESSORIES_WEAPON_DOUBLE = loadImages([
    "accessory_weapon_double.png"])
GR_ACCESSORIES_WEAPON_MINIGUN = loadImages([
    "accessory_weapon_minigun.png"])
GR_ACCESSORIES_WEAPON_LAUNCHER = loadImages([
    "accessory_weapon_launcher.png"])
GR_ACCESSORIES_WEAPON_THROWER = loadImages([
    "accessory_weapon_thrower.png"])
GR_ACCESSORIES_COIN = loadImages([
    "coin_1.png", 
    "coin_2.png",
    "coin_3.png",
    "coin_4.png"])
GR_ACCESSORIES_POWERUP = loadImages([
    "powerup_1.png",
    "powerup_2.png",
    "powerup_3.png",
    "powerup_4.png"])

GR_ACCESSORIES_SHIELD = loadImages([
    "shield_1.png",
    "shield_2.png",
    "shield_3.png",
    "shield_4.png"])

# Backgrounds and parallaxes
GR_BACKGROUND_STARS = loadImages(["stars_background.png"])

GR_PARALLAX_TOR = loadImages(["tor_parallax.png"])
GR_BACKGROUND_TOR = loadImages(["tor_background.png"])

GR_PARALLAX_STONE = loadImages(["stone_parallax.png"])
GR_BACKGROUND_STONE = loadImages(["stone_background.png"])
GR_EFFECT_SPLINTER_TOR = loadImages(["splinter_tor.png"])
GR_EFFECT_SPLINTER_STONE = loadImages(["splinter_stone.png"])
GR_EFFECT_SPLINTER_TECH = loadImages(["splinter_tech.png"])



# Load sounds
snd_laser = loadSound("laser1.ogg", 0.15)
snd_laser_minigun = loadSound("laser3.ogg", 0.20)
snd_laser_enemy = loadSound("laser2.ogg", 0.3)
snd_player_death = loadSound("defeated.ogg", 0.8)
snd_enemy_death = loadSound("hit1.ogg", 0.8)
snd_small_explo = loadSound("hit3.ogg", 0.3)
snd_medium_explo = loadSound("hit4.ogg", 0.5)
snd_coin = loadSound("coin.ogg", 0.3)
snd_wall_hit = loadSound("wallbump.ogg", 0.5)
snd_wall_destroy = loadSound("wall_explode.ogg", 0.8)

# Load music
music_star = [
    "Starmusic_gameplay.mp3",
    "Starmusic_boss.mp3"]

music_planet = [
    "Planetmusic_gameplay.mp3",
    "Planetmusic_boss.mp3"]

music_solar = [
    "Solarmusic_gameplay.mp3",
    "Solarmusic_boss.mp3"]