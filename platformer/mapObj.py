from gameObject import GameObject
from constants import *
import math
from tiles import *

# self.filepath = filepath
# self.image = pygame.image.load(self.filepath)
# self.image = pygame.transform.scale(self.image, (self.w, self.h))
# screen.blit(self.image, pygame.Rect(self.x, self.y, self.w, self.h ))
# self.image = pygame.image.load(self.filepath)

class Player(GameObject):
    
    def __init__(self,level):
        
        super().__init__(level.playerSpawn[0],level.playerSpawn[1])
        
        self.color = GREEN
        self.g = 1
        self.w = 30
        self.h = 30
        self.grounded = False
        self.walled = False
        self.jumpVel = 20
        self.maxXVel = 8
        self.leftPress = False
        self.rightPress = False
        self.lastPress = ""
        self.genFilepath = "assests/VirtualGuy/Jump.png"
        self.image = pygame.image.load(self.genFilepath)
        self.imageRight = pygame.transform.scale(self.image, (self.w, self.h))
        self.imageLeft = pygame.transform.flip(self.imageRight, True, False)
        self.lastImage = self.imageRight
        
        
                
    def movementPress(self, direction, pressed):     
        if direction == "right":
            self.rightPress = pressed
        else:
            self.leftPress = pressed
            
        self.lastPress = direction
        

                       
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.yv -= self.jumpVel
            
    def update(self):
        
        if self.rightPress and not self.leftPress:
            self.xv = self.maxXVel
        elif not self.rightPress and self.leftPress:
            self.xv = -self.maxXVel
        elif self.rightPress and self.leftPress:
            if self.lastPress == "right":
                self.xv = self.maxXVel
            else:
                self.xv = -self.maxXVel
        else:
            self.xv = 0
            
            
        
        if not self.grounded:
            self.yv += self.g
            self.y += self.yv
        if not self.walled:    
            self.x += self.xv
             
            
      
    def draw(self):
        if self.xv > 0:
            screen.blit(self.imageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.imageRight
        elif self.xv < 0:
            screen.blit(self.imageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.imageLeft
        elif self.xv == 0:
            screen.blit(self.lastImage, pygame.Rect(self.x, self.y, self.w, self.h ))
            

      
class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@"}
        self.level = []
        self.playerSpawn = [0,0]
        file = open(self.filePath, "r")
        
        for x in file:
            self.level.append(list(x[:-1]))     
        file.close()
        
        self.widthNum = len(self.level[0])
        self.heightNum = len(self.level)
        self.tileWidth = math.floor(width/self.widthNum)
        self.tileHeight = math.floor(height/self.heightNum)
        
        offset = (width-(self.widthNum)*(self.tileWidth))//2
        
        for y in range(self.heightNum):
            for x in range(self.widthNum):
                
                tileChar = self.level[y][x]
           
                if tileChar == self.mapKey["air"]:
                    self.level[y][x] = Air(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
                elif tileChar == self.mapKey["player"]:
                    self.playerSpawn[0] = x*self.tileWidth+offset
                    self.playerSpawn[1] = y*self.tileHeight+offset
                    self.level[y][x] = Air(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
                elif tileChar == self.mapKey["wall"]:
                    self.level[y][x] = Block(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
              
        
    def update(self):
        for row in self.level:
            for tile in row:
                tile.update()
        
    def draw(self):
        for row in self.level:
            for tile in row:
                tile.draw()

