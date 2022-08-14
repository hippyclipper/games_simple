import pygame
import random
import math
#==========================================================================================================================
screenScale = 8
width = int(100 * screenScale)
height = width//1.25
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
WHITE = (250, 250, 250)
BACKGROUND = (5, 5, 5)
COLORLIST = [RED, GREEN, BLUE]
done = False

# self.idleFilePath = "assests/VirtualGuy/Idle(32x32).png"
# self.idleSheet = pygame.image.load(self.idleFilePath)
# self.idleframeNum = 10
# self.idleSheetSize = self.idleSheet.get_size()
# self.idleImages = []
# for x in range(self.idleframeNum):
# self.idleImages.append(self.idleSheet.subsurface(pygame.Rect(5+(x*22)+(x*10),6,22,26)))
# self.fallFilepath = "assests/VirtualGuy/Fall.png"
# self.fallImage = pygame.image.load(self.fallFilepath)
# self.fallImage = self.fallImage.subsurface(pygame.Rect(5,6,23,26)) 
# self.fallImage = pygame.transform.smoothscale(self.fallImage, (self.w, self.h)) 
# self.fallImageLeft = pygame.transform.flip(self.fallImageRight, True, False)
# screen.blit(self.cloudImage, pygame.Rect(self.x, self.y, self.w, self.h ))
# pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
# self.font = pygame.font.SysFont('arial', 80)
# self.textScore = self.font.render(str(self.scoreInt),True,self.color)
# self.textScoreLocation = self.textScore.get_rect(center = screen.get_rect().center)
# rect2 = pygame.Rect(square.x, square.y, square.w, square.h )
# rect2.colliderect(rect1)

#todo
#chunks 250x250
#grass (everywhere)
#camera movement (world movement)
#flowers (perlin noise patches)
#rock (collision)
#trees (collison, perlin noise)
#lakes (boarders)
#animal/creater


# https://pixelmochii.itch.io/mochii-plains
# https://opengameart.org/content/the-field-of-the-floating-islands

class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0 
        self.yv = 0
        self.r = 10
        self.w = 10
        self.h = 10
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
  
  
  
        
           
class Game:
    
    def __init__(self):
        self.testObj = GameObject(width//2, height//2)
        
    def buttonEvent(self, direction, pressed):
        pass
        
    def handleCollisons(self):
        pass
        
    def update(self):
        self.testObj.update()
    
    def draw(self):
        self.testObj.draw()
        
        
game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True
            
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            game.buttonEvent("space", True)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            game.buttonEvent("left", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            pass
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            pass
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            game.buttonEvent("up", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            pass
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            game.buttonEvent("down", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            pass   
                   
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#==========================================================================================================================
pygame.display.quit()
pygame.quit()    
        
        
        
        
