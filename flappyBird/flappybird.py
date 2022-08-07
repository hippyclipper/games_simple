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

class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0 
        self.yv = 0
        self.r = 10
        self.color = WHITE
        self.g = 1
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Bird(GameObject):
    
    def __init__(self):
        super().__init__(width//4, height//2)
        self.jumpV  = 25
        
    def jump(self):
        self.yv = -self.jumpV
        
    def handlePress(self, direction, pressed):
        if direction == "space" and pressed:
            self.jump()
            
    def update(self):
        self.yv += self.g
        self.y += self.yv
        
class Ground(GameObject):

    def __init__(self):
        self.h = 10
        super().__init__(0,height-self.h)
        self.w = width
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
        
class Pipe(GameObject):
    
    def __init__(self,x,y,h):
        super().__init__(x,y)
        self.w = 10
        self.h = h
               
    def update(self):
        self.x -= 1
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))

class Pipes(GameObject):
    
    def __init__(self):
        super().__init__(width,0)
        self.pipes = []
        self.gapSize = 100
        self.addPipe()
    
    def addPipe(self):
        randY = random.randint(0,height-self.gapSize)
        pipe1 = Pipe(width, 0, randY)
        pipe2 = Pipe(width, self.gapSize+randY, height-(self.gapSize+randY) )
        self.pipes.append(pipe1)
        self.pipes.append(pipe2)
        
    def update(self):
        for pipe in self.pipes:
            pipe.update()
            
    def draw(self):
        for pipe in self.pipes:
            pipe.draw()
        
class Game:
    
    def __init__(self):
        self.bird = Bird()
        self.pipes = Pipes()
        self.ground = Ground()
        
    def buttonEvent(self, direction, pressed):
        self.bird.handlePress(direction, pressed)
        
    def handleCollisons(self):
        pass
        
    def update(self):
        self.bird.update()
        self.pipes.update()
        self.ground.update()
    
    def draw(self):
        self.bird.draw()
        self.pipes.draw()
        self.ground.draw()
        
        
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
        
        
        
        