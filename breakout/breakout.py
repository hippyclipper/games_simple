import pygame
import random
import math

screenScale = 8
width = int(100 * screenScale)
height = width
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BACKGROUND = (5, 5, 5)
WHITE = (255,255,255)
COLORLIST = [RED, GREEN, BLUE]
done = False

#==========================================================================================================================

class GameObject:
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.xv = 0 
        self.yv = 0
        self.maxV = 10
        self.r = 10
        self.color = WHITE
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)     

#==========================================================================================================================
        
class Ball(GameObject):
    
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        
#==========================================================================================================================
        
class Square(GameObject):
    
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y 
        self.h = 10
        self.w = 150
        
    def draw(self):
        
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
        
#==========================================================================================================================
        
class Player(Square):
    def __init__(self):
        super().__init__(width//2, height)
        self.x -= (self.w//2)
        self.y -= self.h+10
        self.left = False
        self.right = False
    
    def update(self):
        
        if self.x+self.xv < 0 or self.x+self.xv > width-(self.w):
            return 
        self.x += self.xv
        
    def moveLeft(self):
        self.left = True
        self.xv = -self.maxV
    
    def moveRight(self):
        self.right = True
        self.xv = self.maxV
        
    def stop(self, direction):

        if direction == "right":
            self.right = False
        else:
            self.left = False

        if not self.left and not self.right:
            self.xv = 0
        elif self.left:
            self.xv = -self.maxV
        else:
            self.xv = self.maxV
            
    def handleEvent(self,direction,pressed):
        
        if direction == "left" and pressed:
            self.moveLeft()
        elif direction =="right" and pressed:
            self.moveRight()
        elif direction in ["right", "left"] and not pressed:
            self.stop(direction)
        
#==========================================================================================================================
        
class Game:
    
    def __init__(self):
        self.ball = Ball(width//2, height//2)
        self.player = Player()
        self.objects = [self.ball, self.player]
    
    def buttonEvent(self, direction, pressed):
        self.player.handleEvent(direction, pressed)
        
    def update(self):
        for obj in self.objects:
            obj.update()
      
    def draw(self):
        for obj in self.objects:
            obj.draw()
       
#==========================================================================================================================
        
game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            pass
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            game.buttonEvent("left", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            game.buttonEvent("left", False)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", False)
            
    game.draw()
    game.update()      
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
    
pygame.display.quit()
pygame.quit()    
