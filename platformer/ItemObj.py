from gameObject import GameObject
from constants import *
import math
#32 pixels from one side to the other
class Item(GameObject):
    
    def __init__(self,x,y,w,h):
        super().__init__(x,y)
        self.filepath = "./assests/Strawberry.png"
        self.w = w
        self.h = h
        self.spriteSheet = pygame.image.load(self.filepath)#.convert_alpha()
        self.sheetSize = self.spriteSheet.get_size()
        self.pixelOffset = 32
        self.numPic = 0
        self.frameWait = 5
        self.counter = 0
        self.spriteNum = 17
        self.ix = self.sheetSize[1]*.25
        self.iy = self.sheetSize[1]*.25
        self.iw = (self.sheetSize[0]//17) * .5
        self.ih = self.sheetSize[1]*.6
        self.images = []
        
        for image in range(self.spriteNum):
            self.images.append(self.spriteSheet.subsurface(pygame.Rect(self.ix+(image*self.pixelOffset), self.iy, self.iw, self.ih)))
            
        self.scale = .6
        
        self.images = [pygame.transform.smoothscale(x, (self.w*self.scale, self.h*self.scale)) for x in self.images]
        
        self.x -= self.images[0].get_width()//2
        self.y -= self.images[0].get_height()//2
        
    def update(self):

        if self.numPic >= 16:
            self.numPic = 0
        else:
            if self.counter % self.frameWait == 0:  
                self.numPic += 1        
        self.counter += 1        

              
    def draw(self):
        screen.blit(self.images[self.numPic], pygame.Rect(self.x, self.y, self.w, self.h))
        
class Items(GameObject):
    
    def __init__(self, level):
        super().__init__(0,0)
        self.items = []
        for point in level.items:
            self.items.append(Item(point[0],point[1],level.tileWidth,level.tileHeight))
            
    def update(self):
        for item in self.items:
            item.update()
            
    def draw(self):
        for item in self.items:
            item.draw()