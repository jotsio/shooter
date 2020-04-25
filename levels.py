import random
from inits import *

#Level global settings
gridsize = 64

# Define map
level1_map = [
".....................",
".....................",
".....................",
".....................",
".....................",
"#...................#",
"##.................##",
"##.................##",
"##.................##",
"##.................##",
"##.................##",
"#.....#............##",
"##....#...#........##",
"###.....X.........###",
"###..#.....#......###",
"#.....#####.........#",
".....................",
".....................",
".....................",
"#...................#",
"##.................##",
"###...............###",
"##.................##",
"#...................#",
"#...................#",
"#.........#..X......#",
".........##..........",
"........####.........",
".........##..........",
".......#####.........",
"##................###",
"#####..........######",
"######........#######",
"########.....########",
"#########....########",
"#########....########",
"#########.....#######",
"#########......######",
"#########...X...#####",
"#########......######",
"#########.....#######",
"########.....########",
"#######.....#########",
"#######.....#########",
"########....#########",
"########.....########",
"#########....########",
"########.....########",
"######.......########",
"########.....########",
"########..X..########",
"########......#######",
"#####...........#####",
"##.................##",
"#...#............#..#",
"#...#....X......###.#",
"#...#............#..#",
"##..#..............##",
"#..#X#.........X..###",
"##..#..............##",
"#...................#",
"#...................#",
"#....X..............#"
]

level2_map = [
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".............########",
"......###############",
".X..#################",
"....###.X..##########",
"....###..X.##########",
"....###....##########",
".....##.X..##########",
"#.....#....##########",
"#.....###############",
"##.........##########",
"##.........##########",
"###........##########",
"#######....##########",
"#######.....#########",
"########....#########",
"#####..##....########",
"#####..##.....#######",
"########......#######",
"###..###......#######",
"###..##......########",
"########.....########",
"#####..##.....#######",
"#####..##......######",
"##########.....######",
"####..#####......####",
"####..######.....####",
"#############.....###",
"#############......##",
"##############...X..#",
"###############......",
"################.....",
"#################..X.",
"#################....",
"########.########....",
"#######...#######....",
"########.####.###....",
"############...##....",
"#############.###....",
"#########.#######....",
"########...######....",
"#########.######.....",
"###############......",
"########............#",
"##.................##",
"##...X.X.X.........##",
"##.................##",
"##.................##",
"##.................##",
"##.......X.X.X.....##",
"##.................##",
"##.................##",
"##.................##",
"##.................##",
"########..X.#########",
"########....#########",
"#....##......##....##",
"#...##........##...##",
"#..##..........##..##",
"#.##............##.##",
"###..............####",
"##................###",
"#..................##",
"....................#"
]

level3_map = [
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
"..X..X..X..X..X..X...",
"...X..X..X..X..X.....",
".....................",
".....................",
".....................",
".......X.............",
"###########..########",
"...........X.........",
".....................",
".....................",
"######..#############",
".....................",
"........X..X.........",
".....................",
".....................",
"..............X......",
"############....#####",
".###...#...#....#....",
"..##...#.X.#....#....",
"...#...#...#....#....",
"...#...#...#....#....",
"...#...#...#....#....",
"...#...#...#....#....",
"...#...#...#....#....",
"...#.X.#...#....#....",
"...#...#...#....#....",
".......#...#.........",
"...........X.........",
".....................",
".....................",
".....................",
"#########..##########",
"########....#########",
"######.X....X.#######",
"#####..........######",
"####.....##.....#####",
"###.....####.....####",
"##.....######.....###",
"#.....########.....##",
"..........#.........#",
"..........#..........",
".........###.........",
"........#####........",
".........###.........",
"..........#..........",
".....................",
".....................",
".....................",
"....................."
]

level4_map = [
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
"..X..X.........X..X..",
".....................",
"X..X..X..X..X..X..X..",
".....................",
"#########...#########",
".....................",
".....................",
"..........###########",
"..........##..###..##",
"....XX....#...XXX...#",
"..........##..###..##",
".X......X.###########",
".....................",
".....................",
"#########...#########",
".X.................X.",
".....................",
]

level_test_map = [
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
"#########....########",
"##########..#########",
"##########..#########",
"##########..#########",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
"........X............",
".......X.............",
"......X..............",
".....X...............",
"....X................",
"...X.................",
"..X..................",
".X...................",
"X....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
".....................",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
"##########..#########",
".....................",
".....................",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
"#...................#",
".....................",
".....................",
]

#Walls class
class Walls:
    def __init__(self, map, tiles):
        self.map = self.levelToList(map)  
        self.img = tiles
        self.start_point = -len(self.map) * gridsize
        self.rect = pygame.Rect(0, self.start_point, gridsize, gridsize) 

    # Convert levels to lists
    def levelToList(self, map):
        i = 0
        while i < len(map):
            map[i] = list(map[i])
            i += 1
        return map

    def defineBlock(self, row, col):
        block = 0
        this = self.map[row][col]
        up = "#"
        down = "#"
        left = "#" 
        right = "#"
        if row > 0:
            up = self.map[row-1][col]
        if row < len(self.map)-1:
            down = self.map[row+1][col]
        if col > 0:
            left = self.map[row][col-1]
        if col < len(self.map[row])-1:
            right = self.map[row][col+1]
        if this == "#":
            if up == "#" and  down == "#" and left == "#" and  right == "#":
                block = 0
            elif up != "#" and  down != "#" and left != "#" and  right != "#":
                block = 1
            elif up != "#" and  down != "#" and left == "#" and  right == "#":
                block = 2
            elif up == "#" and  down == "#" and left != "#" and  right != "#":
                block = 3
            elif up != "#" and  down == "#" and left != "#" and  right != "#":
                block = 4
            elif up == "#" and  down != "#" and left != "#" and  right != "#":
                block = 5
            elif up != "#" and  down != "#" and left != "#" and  right == "#":
                block = 6
            elif up != "#" and  down != "#" and left == "#" and  right != "#":
                block = 7
            elif up != "#" and  down == "#" and left == "#" and  right == "#":
                block = 8
            elif up == "#" and  down != "#" and left == "#" and  right == "#":
                block = 9
            elif up == "#" and  down == "#" and left != "#" and  right == "#":
                block = 10
            elif up == "#" and  down == "#" and left == "#" and  right != "#":
                block = 11
            elif up != "#" and  down == "#" and left != "#" and  right == "#":
                block = 12
            elif up != "#" and  down == "#" and left == "#" and  right != "#":
                block = 13
            elif up == "#" and  down != "#" and left == "#" and  right != "#":
                block = 14
            elif up == "#" and  down != "#" and left != "#" and  right == "#":
                block = 15
            else:
                block = 0
        return block

    def draw(self, offset, screen):
        self.screen = screen
        self.offset = offset
        self.rect.y += self.offset
        # Loop rows
        k = 0
        while k < len(self.map):
            # Draw one row of blocks and draw graphics if wall exists
            if self.rect.y >= -gridsize and self.rect.y <= height:
                i = 0 
                while i < len(self.map[k]):
                    # Draw right block on screen
                    if self.map[k][i] == "#":
                        self.screen.blit(self.img[self.defineBlock(k,i)], self.rect)
                    # create enemy on screen
 #                   if self.map[k][i] == "X" and self.rect.y == -gridsize:
 #                       enemy = EnemyShip(self.rect.x, self.rect.y)
                    # select which wall asset to use
                    self.rect.x += gridsize
                    i += 1
                self.rect.x = 0
            k += 1
            self.rect.y += gridsize
        self.rect.y = self.start_point
    
    # Checks collision to walls for certain rectangle
    def checkCollision(self, obj_rect, offset):
        self.offset = offset
        k = 0
        self.rect.y += self.offset
        #loop rows
        while k < len(self.map):
            #check one row of blocks and mark collision if wall exists
            if self.rect.y >= -gridsize and self.rect.y <= height:
                i = 0
                while i < len(self.map[k]):
                    if self.map[k][i] == "#":
                        if self.rect.colliderect(obj_rect):
                            self.rect.y = self.start_point
                            return (i, k)
                    self.rect.x += gridsize
                    i += 1            
                self.rect.x = 0
            k += 1
            self.rect.y += gridsize
        self.rect.y = self.start_point

    # Removes defined wallblock from level
    def removeBlock(self, col, row):
        self.map[row][col] = "."

    # Gives a list of enemies from current row
    def getEnemies(self, offset):
        y = self.start_point
        y += offset
        x = 0
        enemy_list = []
        # Loop rows
        k = 0
        while k < len(self.map):
            if y == -gridsize:
                i = 0 
                while i < len(self.map[k]):
                    # Draw right block on screen
                    if self.map[k][i] == "X":
                        position = (x, y)
                        enemy_list.append(position) 
                    x += gridsize
                    i += 1
                x = 0
            k += 1
            y += gridsize
        return enemy_list 

            

# Animated star background
class StarField:
    def __init__(self, amount):
        self.n = amount
        self.spd = 0.5
        self.y = [0.0] * amount
        self.x = [0.0] * amount
        self.z = [0.0] * amount
        self.color = [0,0,0] * amount
        self.speed = [0.0] * amount

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

    def draw(self, screen): 
        self.screen = screen
        i = 0
        while i < self.n:
            self.y[i] += self.speed[i]
            if self.y[i] > height: self.y[i] = 0
            pygame.gfxdraw.pixel(self.screen, self.x[i], int(self.y[i]), self.color[i])
            i += 1

# Create levels
levels = [
    Walls(level1_map, wallset_tech), 
    Walls(level2_map, wallset_stone),  
    Walls(level3_map, wallset_tech),
    Walls(level4_map, wallset_tech)
    ]
