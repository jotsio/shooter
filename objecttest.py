#object class
class Object:

    def __init__(self):
        print ("Object is ready")
        self.x = 300
        self.y = 200
        self.dx = 0
        self.dy = 0
    
#player class
class Player(Object):   

    def whoisThis(self):
        print ("Player")

        
playerShip = Player()
print (playerShip.x)