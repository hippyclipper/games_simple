from gameObject import GameObject
from constants import * 


class Tile(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = RED
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
    

class Map(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.filePath = "./map.txt"
        self.mapKey = {"wall": "#", "air": ".", "player": "$", "end": "@"}
        self.widthNum = 0
        self.heightNum = 0
        self.level = []
        file = open(self.filePath, "r")
        
        for x in file:
            self.heightNum += 1
            self.widthNum = max(self.widthNum, len(x))
        self.tileW = width/self.widthNum
        self.tileH = height/self.heightNum
        file.close()
        file = open(self.filePath, "r")
        for x,line in enumerate(file):
            self.level.append([])
            for y,tile in enumerate(line):
                self.level[x].append(Tile(x,y))
                
        file.close()
        
    def update(self):
        for row in self.level:
            for tile in row:
                tile.update()
        
    def draw(self):
        for row in self.level:
            for tile in row:
                tile.draw()
        
        
                                 
            
        
