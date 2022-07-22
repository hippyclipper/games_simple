from gameObject import GameObject
from constants import *
import math
from tiles import *


class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@", "strawberry": "S"}
        self.level = []
        self.playerSpawn = [0,0]
        self.items = []
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
                elif tileChar == self.mapKey["end"]:
                    self.level[y][x] = End(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
                elif tileChar == self.mapKey["strawberry"]:
                    self.level[y][x] = Air(x*self.tileWidth+offset, y*self.tileHeight+offset, self.tileWidth, self.tileHeight)
                    self.items.append((x*self.tileWidth+offset+(self.tileWidth//2),y*self.tileHeight+offset+(self.tileHeight//2)))
        
    def update(self):
        for row in self.level:
            for tile in row:
                tile.update()
        
    def draw(self):
        for row in self.level:
            for tile in row:
                tile.draw()

