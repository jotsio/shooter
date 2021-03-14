import random
from inits import *
from level_test import *
from level1 import *
from level2 import *
from level3 import *
from level4 import *
from level5 import *
from level6 import *

#Level global settings
gridsize = 64

#Walls class
class Walls:
    def __init__(self, features):
        self.reset(features)

    def reset(self, features):
        self.map = self.levelToList(features["map"])
        self.img = features["imageset"]  
        self.music = features["music"]
        self.width = width
        self.height = height - 32
        self.start_point = -len(self.map) * gridsize
        self.rect = pygame.Rect(0, self.start_point, gridsize, gridsize) 
        self.level_finished = False
        self.background = features["background"]()
        self.hilight = 0
    
    # Convert levels to lists
    def levelToList(self, map):
        i = 0
        list_map = []
        while i < len(map):
            list_map.append(list(map[i]))
            i += 1
        return list_map

    def checkSolid(self, character):
        result = False
        solidlist = ["#", "Y", "U"]
        for i in solidlist:
            if character == i: 
                result = True
        return result

    def defineBlock(self, row, col):
        block = 0
        up = True
        down = True
        left = True 
        right = True

        if row > 0:
            up = self.checkSolid(self.map[row-1][col])
        if row < len(self.map)-1:
            down = self.checkSolid(self.map[row+1][col])
        if col > 0:
            left = self.checkSolid(self.map[row][col-1])
        if col < len(self.map[row])-1:
            right = self.checkSolid(self.map[row][col+1])

        if up == True and  down == True and left == True and  right == True:
            block = 0
        elif up == False and  down == False and left == False and  right == False:
            block = 1
        elif up == False and  down == False and left == True and  right == True:
            block = 2
        elif up == True and  down == True and left == False and  right == False:
            block = 3
        elif up == False and  down == True and left == False and  right == False:
            block = 4
        elif up == True and  down == False and left == False and  right == False:
            block = 5
        elif up == False and  down == False and left == False and  right == True:
            block = 6
        elif up == False and  down == False and left == True and  right == False:
            block = 7
        elif up == False and  down == True and left == True and  right == True:
            block = 8
        elif up == True and  down == False and left == True and  right == True:
            block = 9
        elif up == True and  down == True and left == False and  right == True:
            block = 10
        elif up == True and  down == True and left == True and  right == False:
            block = 11
        elif up == False and  down == True and left == False and  right == True:
            block = 12
        elif up == False and  down == True and left == True and  right == False:
            block = 13
        elif up == True and  down == False and left == True and  right == False:
            block = 14
        elif up == True and  down == False and left == False and  right == True:
            block = 15

        return block

    # Parses the level map and draws graphics if wall exists
    def draw(self, offset, screen, scroll_speed):
        # Background
        if self.hilight > 0:
            self.background.hilightOn()
            self.hilight -= 1
        else:
            self.background.hilightOff()

        self.background.draw(scroll_speed, screen)
        # Blocks
        rect = pygame.Rect(0, self.start_point, gridsize, gridsize)
        rect.y += offset
        k = 0
        while k < len(self.map):
            if rect.y >= -gridsize and rect.y <= height:
                i = 0 
                while i < len(self.map[k]):
                    if self.map[k][i] == "#":
                        # Draw from secondary tiles
                        if randomlist[(k * 21 + i) % 100] >= 10:
                            screen.blit(self.img[self.defineBlock(k,i) + 16], rect)
                        # Draw from normal tiles
                        else:
                            screen.blit(self.img[self.defineBlock(k,i)], rect)
                    rect.x += gridsize
                    i += 1
                rect.x = 0
            k += 1
            rect.y += gridsize

        
    # Parses the level map and returns block position if wall is found

    def checkCollision(self, obj_rect, offset):
        rect = pygame.Rect(0, self.start_point, gridsize, gridsize)
        rect.y += offset
        k = 0
        while k < len(self.map):
            if rect.y >= update_offset_up and rect.y <= height + update_offset_down:
                i = 0 
                while i < len(self.map[k]):
                    if self.map[k][i] == "#":
                        if rect.colliderect(obj_rect):
                            return (i, k)
                    rect.x += gridsize
                    i += 1            
                rect.x = 0
            k += 1
            rect.y += gridsize

    def locateCollision(self, obj_rect, offset):
        rect = pygame.Rect(0, self.start_point, gridsize, gridsize)
        rect.y += offset
        k = 0
        while k < len(self.map):
            if rect.y >= -gridsize and rect.y <= height:
                i = 0 
                while i < len(self.map[k]):
                    if self.map[k][i] == "#":
                        if rect.colliderect(obj_rect):
                            return rect
                    rect.x += gridsize
                    i += 1            
                rect.x = 0
            k += 1
            rect.y += gridsize

    # Removes defined wallblock from level
    def removeBlock(self, col, row):
        self.map[row][col] = "."

    # Gives a list of enemy characters from current row
    def getEnemies(self, offset):
        y = self.start_point
        y += offset
        x = 0
        enemy_list = []
        # Loop rows
        k = 0
        while k < len(self.map):
            if y >= -gridsize:
                i = 0 
                while i < len(self.map[k]):
                    # Give the enemy positions and style as list
                    character = self.map[k][i]
                    if character != "#" and character != ".":
                        position = (x, y, character)
                        enemy_list.append(position)
                        self.removeBlock(i, k)
                    x += gridsize
                    i += 1
                x = 0
            k += 1
            y += gridsize
        return enemy_list 

    def flashBg(self):
        self.background.hilightOn()
        self.hilight = 8

# Background, starfield
class BgStarField:
    def __init__(self):
        self.n = 250
        self.spd = 0.5
        self.y = [0.0] * self.n
        self.x = [0.0] * self.n
        self.z = [0.0] * self.n
        self.color = [0,0,0] * self.n
        self.speed = [0.0] * self.n
        self.bg_color = color_bg_stars_default

        #Create star a random.rect and speed
        i = 0
        while i < self.n:
            self.y[i] = random.randrange(0, height)
            self.x[i] = random.randrange(0, width)
            rnd = random.random()
            self.z[i] = rnd * rnd * 255
            c = self.z[i]
            self.color[i] = c, c, c
            self.speed[i] = c / 255.0 * self.spd
            i += 1

    def hilightOn(self):
        self.bg_color = color_bg_stars_hilight

    def hilightOff(self):
        self.bg_color = color_bg_stars_default

    def draw(self, scroll_speed, screen): 
        screen.fill(self.bg_color)
        i = 0
        while i < self.n:
            self.y[i] += self.speed[i] * scroll_speed
            if self.y[i] > height: self.y[i] = 0
            pygame.gfxdraw.pixel(screen, self.x[i], int(self.y[i]), self.color[i])
            i += 1

# Background, clouds
class BgClouds:
    def __init__(self):
        self.layer_1 = BgLayer(GR_BACKGROUND_CLOUDS_TOP[0], 0.5)
        self.layer_2 = BgLayer(GR_BACKGROUND_CLOUDS_BOTTOM[0], 0.25)
        self.bg_color = color_bg_clouds_default

    def hilightOn(self):
        self.bg_color = color_bg_clouds_hilight

    def hilightOff(self):
        self.bg_color = color_bg_clouds_default

    def draw(self, scroll_speed, screen): 
        screen.fill(self.bg_color)
        self.layer_2.draw(screen, scroll_speed)
        self.layer_1.draw(screen, scroll_speed)

class BgLayer:
    def __init__(self, img, speed):
        self.image = img
        self.height = self.image.get_height()
        self.speed = speed
        self.offset = 0

    def draw(self, screen, scroll_speed):
        self.offset += scroll_speed * self.speed 
        if self.offset < 0:
            self.offset += heigth
        if self.offset > self.height:
            self.offset = 0
        screen.blit(self.image, (0, round(self.offset)))
        screen.blit(self.image, (0, round(self.offset-height)))


# Level parameters
levels = [
    {
    "map":level1_map, 
    "imageset": GR_WALLSET_TOR, 
    "background": BgClouds, 
    "music": music_planet
    },
    {
    "map":level2_map, 
    "imageset": GR_WALLSET_STONE, 
    "background": BgClouds, 
    "music": music_star
    },
    {
    "map":level3_map, 
    "imageset": GR_WALLSET_TOR, 
    "background": BgStarField, 
    "music": music_solar
    },
    {
    "map":level4_map, 
    "imageset": GR_WALLSET_STONE, 
    "background": BgStarField, 
    "music": music_planet
    },
    {
    "map":level5_map, 
    "imageset": GR_WALLSET_TECH, 
    "background": BgClouds, 
    "music": music_star
    },
    {
    "map":level6_map, 
    "imageset": GR_WALLSET_TECH, 
    "background": BgStarField, 
    "music": music_solar
    }]