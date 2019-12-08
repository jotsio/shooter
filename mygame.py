import sys, pygame
pygame.init()

#object class
class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        print("Object is ready")

#particle class
class Particle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy  
        print("Particle is ready")  

#player class
class PlayerShip:
    def __init__(self, x, y):
        self.startPos = [x, y]
        self.speed = [0.000, 0.000]  
        self.img = pygame.image.load("assets/ship_default.png")
        self.rect = self.img.get_rect()
        self.rect = self.rect.move(x, y)
        self.maxSpeedX = 4
        self.maxSpeedY = 2
        self.frictionX = 0.1
        self.frictionY = 0.1
        print("Player is ready")  
    
    # Passive movement
    def move(self):
        self.rect = self.rect.move(self.speed)
        # Horizontal friction
        if self.speed[0] > 0 :
            self.speed[0] -= self.frictionX
        if self.speed[0] < 0 :
            self.speed[0] += self.frictionX
        # Vertical friction
        if self.speed[1] > 0 :
            self.speed[1] -= self.frictionY
        if self.speed[1] < 0 :
            self.speed[1] += self.frictionY
    
    # Vertical acceleration
    def setSpeedX(self, amount):
        self.speed[0] += amount
        if self.speed[0] > self.maxSpeedX :
            self.speed[0] = self.maxSpeedX
        if self.speed[0] < -self.maxSpeedX :
            self.speed[0] = -self.maxSpeedX

    # Horizontal acceleration
    def setSpeedY(self, amount):
        self.speed[1] += amount
        if self.speed[1] > self.maxSpeedY :
            self.speed[1] = self.maxSpeedY
        if self.speed[1] < -self.maxSpeedY :
            self.speed[1] = -self.maxSpeedY

    def bounceX(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        self.speed[0] = -self.speed[0]
    def bounceY(self):

        self.speed[1] = -self.speed[1]


#define screen

size = width, height = 800, 600
black = 0, 0, 0
screen = pygame.display.set_mode(size)    

# Create player
player = PlayerShip(400,500)
print (player.rect)

clock = pygame.time.Clock()

while clock.tick(120):
    # Keyevents listener
    for event in pygame.event.get():
       if event.type == pygame.QUIT: sys.exit()
    
    pressed = pygame.key.get_pressed()
    player.setSpeedX(pressed[pygame.K_RIGHT]-pressed[pygame.K_LEFT])
    player.setSpeedY(pressed[pygame.K_DOWN]-pressed[pygame.K_UP])
    
    # Player movement
    player.move()

    # bounces from the wall
    if player.rect.left < 0 or player.rect.right > width:
        player.bounceX()
    if player.rect.top < 0 or player.rect.bottom > height:
        player.bounceY()
    

    screen.fill(black)
    screen.blit(player.img, player.rect)
    pygame.display.flip()