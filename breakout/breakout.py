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
        self.maxV = 5
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
        self.maxV = 10
        self.hit = False
        self.waitTime = 30
        self.xv, self.yv = self.calcVector(math.pi*2*.25+random.uniform(-.2,0), self.maxV)
    
    
    
    def restart(self):
        self.xv, self.yv = self.calcVector(math.pi*2*.25+random.uniform(-.2,0), self.maxV)
        self.waitTime = 30
        self.x = width//2
        self.y = height//2
    
    def update(self):
        if self.waitTime > 0:
            self.waitTime -= 1
            return
        
        if self.y > height*2:
            self.restart()
            return
        
        self.x += self.xv
        self.y += self.yv
        
 
            
#==========================================================================================================================
        
class Square(GameObject):
    
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y 
        self.h = 10
        self.w = 150
        self.deleteMe = False
               
    def draw(self):       
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
        
#==========================================================================================================================
        
class Walls:
    
    def __init__(self):
        
        self.top = Square(0,0)
        self.top.w = width
        self.top.h = 40
        self.top.y -= self.top.h
        
        self.left = Square(0,0)
        self.left.w = 40
        self.left.h = height
        self.left.x -= self.left.w
        
        self.right = Square(width,0)
        self.right.w = 40
        self.right.h = height     
        
        self.blocks = [self.right, self.left, self.top]

class Blocks(Walls):
    
    def __init__(self):
        super().__init__()
        self.numRow = 7
        self.numCol = 10
        self.space = 10
        self.w = (width-(self.space*2))//self.numCol
        self.h = 30
        self.blocks = []
        
        for x in range(self.numCol):
            for y in range(self.numRow):
                square = Square((self.space+self.w)*x+self.space, y*(self.h+self.space)+self.space)
                square.w = self.w
                square.h = self.h
                self.blocks.append(square)
        
    def update(self):
        for block in self.blocks:
            if block.deleteMe:
                self.blocks.remove(block)
    
    def draw(self):
        for block in self.blocks:
            block.draw()

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
class CollisionHandler:
    
    def __init__(self):
        pass
    
    def ballAndBlocks(self, ball, blocks):
        for block in blocks.blocks:
            self.ballAndSquare(ball, block)
    
    def ballAndSquare(self, ball, square):
        
        ballRect = pygame.Rect(ball.x-ball.r, ball.y-ball.r, ball.r*2, ball.r*2)
        squareRect = pygame.Rect(square.x, square.y, square.w, square.h )
        normal = [0, 0]
        collisonAxisIsY = False
        collisonAxisIsX = False
        
        
        ballRect.x += ball.xv
        ballRect.y +=  ball.yv
        
        pygame.draw.rect(screen, RED, ballRect)
        
        if not ballRect.colliderect(squareRect):
            return
        
        ballRect.x -= ball.xv
        
        if not ballRect.colliderect(squareRect):
            collisonAxisIsX = True
            collisonAxisIsY = False
        else:
            collisonAxisIsX = False
            collisonAxisIsY = True
        
        if collisonAxisIsY and ball.yv > 0:
            normal = [0, -1]
        elif collisonAxisIsY and ball.yv <= 0:
            normal = [0, 1]
        elif collisonAxisIsX and ball.xv >= 0:
            normal = [-1,0]
        elif collisonAxisIsX and ball.xv < 0:
            normal = [1,0]
            
        print(ball.y, squareRect.y+squareRect.h)
        square.deleteMe = True
        ball.xv, ball.yv = pygame.math.Vector2([ball.xv,ball.yv]).normalize().reflect(pygame.math.Vector2(normal)) * ball.maxV


#==========================================================================================================================
class Game:
    
    def __init__(self):

        self.ball = Ball(width//2, height//2)
        self.player = Player()
        self.walls = Walls()
        self.blocks = Blocks()
        
        self.collisionHandler = CollisionHandler()
        
    def handleCollisions(self):
        self.collisionHandler.ballAndSquare(self.ball, self.player)
        self.collisionHandler.ballAndBlocks(self.ball, self.walls)
        self.collisionHandler.ballAndBlocks(self.ball, self.blocks)
  
    def buttonEvent(self, direction, pressed):
        self.player.handleEvent(direction, pressed)
        
    def update(self):
        self.handleCollisions() 
        self.ball.update() 
        self.player.update()
        self.blocks.update()
      
    def draw(self):
        self.ball.draw()
        self.player.draw()
        self.blocks.draw()

       
#==========================================================================================================================
        
game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
