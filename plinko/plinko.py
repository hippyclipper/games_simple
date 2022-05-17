import pygame
import random
import math
#==========================================================================================================================
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
WHITE = (250, 250, 250)
BACKGROUND = (5, 5, 5)
COLORLIST = [RED, GREEN, BLUE]
done = False
LEFT_MOUSE = 1
RIGHT_MOUSE = 3
#==========================================================================================================================
class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.g = 2
        self.bounce = 1
        self.xv = 0 
        self.yv = 0
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
        super().__init__(x,y)
#==========================================================================================================================    
class PlayerBall(Ball):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = RED
        
    def update(self):
        self.yv += self.g
        self.x += self.xv
        self.y += self.yv
#==========================================================================================================================        
class PaddleBall(Ball):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = BLUE
#==========================================================================================================================
class BallList(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.balls = []   
             
    def update(self):
        for ball in self.balls:
            ball.update()
            
    def draw(self):
        for ball in self.balls:
            ball.draw()        
#==========================================================================================================================
class PlayerBalls(BallList):
    def __init__(self):
        super().__init__()
        
    def spawnBall(self, x, y, paddleBalls):
        if x > paddleBalls.balls[0].x and x < paddleBalls.balls[paddleBalls.topCol-1].x and paddleBalls.balls[0].y > y:
            self.balls.append(PlayerBall(x,y))
#==========================================================================================================================        
class PaddleBalls(BallList):
    
    def __init__(self):
        super().__init__()
        self.topCol = 3
        self.rows = 10
        self.offsetH = (height//self.rows) * .8
        self.offsetW = (width//self.rows) * .8
        for y in range(self.rows):
            for x in range(self.topCol+y):
                newX = x*self.offsetW+((self.rows-(y/2))*self.offsetW)
                newY = y*self.offsetH
                self.balls.append(PaddleBall(newX, newY))
                
        xoff = self.balls[-1].x - width
        #self.balls[-self.topCol-self.rows+1].color = RED
        yoff = (height - self.balls[-1].y) * .50
        for ball in self.balls:
            ball.x -= xoff
            ball.y += yoff
        xoff = self.balls[-self.topCol-self.rows+1].x//2
        for ball in self.balls:
            ball.x -= xoff

        
#==========================================================================================================================
class Game:
    
    def __init__(self):
        self.paddleBalls = PaddleBalls()
        self.playerBalls = PlayerBalls()
        
        
    def buttonEvent(self, direction, pressed):
        pass
    
    def mouseEvent(self, button, pressed, x, y):
        self.playerBalls.spawnBall(x, y, self.paddleBalls)
        
    def handleCollisons(self):
        pass
        
    def update(self):
        self.paddleBalls.update()
        self.playerBalls.update()
    
    def draw(self):
        self.paddleBalls.draw()
        self.playerBalls.draw()
#==========================================================================================================================        
game = Game()

while not done:
    
    x, y = pygame.mouse.get_pos()
    
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
        
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==  RIGHT_MOUSE:           
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
            game.mouseEvent("left_mouse", True, x, y)
                   
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#==========================================================================================================================
pygame.display.quit()
pygame.quit()    
        
        
        
        
