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
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)      
        
class Paddle(GameObject):
    
    def __init__(self,x,y):
        self.widthScale = 10
        self.paddleV = 10
        super().__init__(x,y)
        self.y -= self.r*self.widthScale//2
        self.up = False
        self.down = False
        
    def update(self):
        
        if self.y < 0 and self.yv < 0:
            return
        elif self.y > height-(self.r*self.widthScale) and self.yv > 0:
            return
        self.y += self.yv
            
        
    def moveUp(self):
        self.up = True
        self.yv = -self.paddleV
    
    def moveDown(self):
        self.down = True
        self.yv = self.paddleV
    
    def stop(self, direction):
        if direction == "up":
            self.up = False
        else:
            self.down = False
            
        if not self.up and not self.down:
            self.yv = 0
        elif self.up:
            self.yv = -self.paddleV
        else:
            self.yv = self.paddleV
        
    def draw(self):
        #[x, y, width, height]
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.r, self.r*self.widthScale ))
        
class LeftPaddle(Paddle):
    def __init__(self,x,y):
        super().__init__(x,y)
           
        
class RightPaddle(Paddle):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x -= self.r
    
class Ball(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.maxVel = 5
        self.xv, self.yv = self.calcVector(random.uniform(-.25*math.pi, .25*math.pi)+[0,math.pi][random.randint(0,1)], self.maxVel)
        
class MidLine(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x -= self.r//2
        self.numSquares = 20
        self.widthScale = 3
        self.color = (220, 220, 220)
        
    def draw(self):
        for x in range(self.numSquares):
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, x*50, self.r, self.r*self.widthScale ))
            
        
  
class Game:
    
    def __init__(self):
        self.paddleLeft = LeftPaddle(0, height//2)
        self.paddleRight = RightPaddle(width, height//2)
        self.ball = Ball(width//2, height//2)
        self.midLine = MidLine(width//2, 0)
        
    def buttonPressed(self, direction, pressed):
        if direction == "down" and pressed:
            self.paddleLeft.moveDown()
        elif direction =="up" and pressed:
            self.paddleLeft.moveUp()
        elif direction in ["up", "down"] and not pressed:
            self.paddleLeft.stop(direction)
        
    def update(self):
        self.paddleLeft.update()
        self.paddleRight.update()
        self.ball.update()
    
    def draw(self):
        self.midLine.draw()
        self.paddleLeft.draw()
        self.paddleRight.draw()
        self.ball.draw()


game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            pass
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            game.buttonPressed("up", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            game.buttonPressed("up", False)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            game.buttonPressed("down", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            game.buttonPressed("down", False)
        
            
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
pygame.display.quit()
pygame.quit()    
