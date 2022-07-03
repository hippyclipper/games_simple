from gameObject import GameObject
from constants import *
import math
from tiles import *





class Player(GameObject):
    def __init__(self,level):
        super().__init__(level.playerSpawn[0],level.playerSpawn[1])
        self.color = GREEN
        self.g = 1
        self.w = 20
        self.h = 20
        self.grounded = False
        self.jumpVel = 22
        self.maxXvel = 5
        
    def move(self, direction):
        if direction == "right":
            self.xv = self.maxXvel
        else:
            self.xv = -self.maxXvel
        
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.yv -= self.jumpVel
            
    def update(self):
        if not self.grounded:
            self.yv += self.g
            self.y += self.yv
        self.x += self.xv

      
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))    

      
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
        
        
                                 
            
        
