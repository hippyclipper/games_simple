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
        self.level = [Tile(height//2, width//2)]
        file = open(self.filePath, "r")
        for x in file:
            self.heightNum += 1
            self.widthNum = max(self.widthNum, len(x))          
        file.close()
        
    def update(self):
        for tile in self.level:
            tile.update()
        
    def draw(self):
        for tile in self.level:
            tile.draw()
        
        
                                 
            
        
