from gameObject import GameObject
from constants import *
import math


class Tile(GameObject):
    
    def __init__(self,x,y,w,h):
        
        super().__init__(x,y)
        self.color = RED
        self.w = w
        self.h = h
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
    
class Block(Tile):
    
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)
        self.filepath = "./assests/Idle.png"
        self.image = pygame.image.load(self.filepath)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
       
    def draw(self):
        screen.blit(self.image, pygame.Rect(self.x, self.y, self.w, self.h ))
        


class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@"}
        self.level = []
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
                self.level[y][x] = Tile(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
                if tileChar == ".":
                    self.level[y][x].color = BLUE
                elif tileChar == "@":
                    self.level[y][x].color = GREEN
                elif tileChar == "#":
                    self.level[y][x] = Block(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)

                    
                
        
    def update(self):
        for row in self.level:
            for tile in row:
                tile.update()
        
    def draw(self):
        for row in self.level:
            for tile in row:
                tile.draw()
        
        
                                 
            
        
