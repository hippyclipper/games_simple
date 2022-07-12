from gameObject import GameObject
from constants import *
import math

class Tile(GameObject):
    
    def __init__(self,x,y,w,h):
        super().__init__(x,y)
        self.color = RED
        self.w = w
        self.h = h
        self.canCollide = False
      
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))

class ImageBlock(Tile):
    
    def __init__(self,x,y,w,h,filepath):
        super().__init__(x,y,w,h)
        self.filepath = filepath
        self.image = pygame.image.load(self.filepath)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def draw(self):
        screen.blit(self.image, pygame.Rect(self.x, self.y, self.w, self.h ))
        
class Block(ImageBlock):
    
    def __init__(self,x,y,w,h):
        self.filepath = "./assests/TerrainBox.png"
        super().__init__(x,y,w,h,self.filepath)
        self.canCollide = True
    
class Air(ImageBlock):
    
    def __init__(self,x,y,w,h):
        self.filepath = "./assests/Blue.png"
        super().__init__(x,y,w,h,self.filepath)
        
class End(ImageBlock):
    
    def __init__(self,x,y,w,h):
        self.filepath = "./assests/End.png"
        super().__init__(x,y,w,h,self.filepath)
        self.air = Air(x, y, w, h)
        
    def draw(self):
        self.air.draw()
        screen.blit(self.image, pygame.Rect(self.x, self.y, self.w, self.h ))
        