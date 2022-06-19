from gameObject import GameObject
from constants import * 


class Tile(GameObject):
    
    def __init__(self,x,y,w,h):
        
        super().__init__(x,y)
        self.color = RED
        self.w = w
        self.h = h
        
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
            self.level.append(x[:-1])     
        file.close()
        #for each charecter in level turn that character into a tile based in the corrasponding descignated tile
        for x in self.level:
            print(x)
        
    def update(self):
        for row in self.level:
            for tile in row:
                tile.update()
        
    def draw(self):
        for row in self.level:
            for tile in row:
                tile.draw()
        
        
                                 
            
        
