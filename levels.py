import random
from inits import *
from classes import *
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
        self.background = LevelBackground(features["background"], features["parallax"], features["shadow"])
        self.splinter = features["splinter"]

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
        self.background.draw(screen, scroll_speed)

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
        
    def createPieces(self, x, y, amount):
        i = 0
        while amount > i:
            NewParticleEffect(x, y, self.splinter)
            i += 1

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

# Background classes
class LevelBackground:
    def __init__(self, background, parallax, shadow):
        self.background = background
        self.parallax = parallax
        self.shadow = shadow
        #self.shadow_image = GR_PLAYER_SHADOW[0]
        #self.shadow_rect = pygame.Rect(0, 0, 64, 64)

    def getPlayerPosition(self, position):
        self.shadow_rect.centerx = position.centerx + 64
        self.shadow_rect.centery = position.centery + 64
    
    def draw(self, screen, scroll_speed): 
        self.background.draw(screen, scroll_speed)
        self.parallax.draw(screen, scroll_speed)
        #if self.shadow == True:
        #    screen.blit(self.shadow_image, self.shadow_rect)
        
        


class BgLayer:
    def __init__(self, img, speed):
        self.image = pygame.transform.scale(img[0], (width, height))
        self.height = self.image.get_height()
        self.speed = speed
        self.offset = 0

    def draw(self, screen, scroll_speed):
        self.offset += scroll_speed * self.speed 
        if self.offset < 0:
            self.offset += self.height
        if self.offset > self.height:
            self.offset = 0
        rows = 0
        drawpoint = self.offset - self.height
        while rows * self.height < height + self.height:
            screen.blit(self.image, (0, round(drawpoint + self.height * rows)))
            rows +=1

class StarLayer:
    def __init__(self, color, speed):
        self.n = 250
        self.speed = speed
        self.y = [0.0] * self.n
        self.x = [0.0] * self.n
        self.z = [0.0] * self.n
        self.color = [color] * self.n
        i = 0
        while i < self.n:
            self.y[i] = random.randrange(0, height)
            self.x[i] = random.randrange(0, width)
            rnd = random.random()
            self.z[i] = rnd * rnd * 0.75 + 0.25
            self.color[i] = round(self.color[i][0] * self.z[i]), round(self.color[i][1] * self.z[i]), round(self.color[i][2] * self.z[i])
            i += 1
    
    def draw(self, screen, scroll_speed):
        i = 0
        while i < self.n:
            self.y[i] += self.z[i] * self.speed * scroll_speed
            if self.y[i] > height: self.y[i] = 0
            pygame.gfxdraw.pixel(screen, self.x[i], int(self.y[i]), self.color[i])
            i += 1

# Level parameters
levels = [
    {
    "map":level1_map, 
    "imageset": GR_WALLSET_TOR, 
    "background": BgLayer(GR_BACKGROUND_TOR, 0.0),
    "parallax": BgLayer(GR_PARALLAX_TOR, 0.25),
    "shadow": False,
    "splinter": GR_EFFECT_SPLINTER_TOR,
    "music": music_planet
    },
    {
    "map":level2_map, 
    "imageset": GR_WALLSET_STONE, 
    "background": BgLayer(GR_BACKGROUND_STONE, 0.4),
    "parallax": BgLayer(GR_PARALLAX_STONE, 0.5),
    "shadow": True,
    "splinter": GR_EFFECT_SPLINTER_STONE,
    "music": music_star
    },
    {
    "map":level3_map, 
    "imageset": GR_WALLSET_TOR, 
    "background": BgLayer(GR_BACKGROUND_TOR, 0.0),
    "parallax": BgLayer(GR_PARALLAX_TOR, 0.25),
    "shadow": False,
    "splinter": GR_EFFECT_SPLINTER_TOR,
    "music": music_solar
    },
    {
    "map":level4_map, 
    "imageset": GR_WALLSET_STONE, 
    "background": BgLayer(GR_BACKGROUND_STONE, 0.4),
    "parallax": BgLayer(GR_PARALLAX_STONE, 0.5),
    "shadow": True,
    "splinter": GR_EFFECT_SPLINTER_STONE,
    "music": music_planet
    },
    {
    "map":level5_map, 
    "imageset": GR_WALLSET_TECH, 
    "background": BgLayer(GR_BACKGROUND_STARS, 0.0),
    "parallax": StarLayer(WHITE, 0.4),
    "shadow": False,
    "splinter": GR_EFFECT_SPLINTER_TECH,
    "music": music_star
    },
    {
    "map":level6_map, 
    "imageset": GR_WALLSET_TECH, 
    "background": BgLayer(GR_BACKGROUND_STARS, 0.0),
    "parallax": StarLayer(WHITE, 0.4),
    "shadow": False,
    "splinter": GR_EFFECT_SPLINTER_TECH,
    "music": music_solar
    }]