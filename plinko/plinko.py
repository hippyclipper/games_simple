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


# TODO
# add coloring to squares
# change color scheme
# add score multipler text
# score
# detect collison of award squares

# detection of collison with squares
# refelection using breakout method

def sign(num):
    if num < 0:
        return -1
    return 1

#==========================================================================================================================
class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.g = .5
        self.bounce = 1
        self.xv = 0 
        self.yv = 0
        self.r = 7
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
        self.friction = .5
        
    def update(self):
        self.yv += self.g
        self.x += self.xv
        self.y += self.yv
        
    def reflectOffPaddle(self, paddle):
        x1 = self.x
        y1 = self.y
        x2 = paddle.x
        y2 = paddle.y
        speed = math.sqrt((x1-x1+self.xv)**2 + (y1-y1+self.yv)**2)
        newXv = x1 - x2
        newYv = y1 - y2
        newV = pygame.math.Vector2([newXv,newYv]).normalize()
        
        if newV[0] == 0:
            newV[0] = .001
        
        self.xv = newV[0] * speed * self.friction
        self.yv = newV[1] * speed * self.friction
        
        
        
        self.x += newV[0] * (self.r + paddle.r)//2
        self.y += newV[1] * (self.r + paddle.r)//2

              
#==========================================================================================================================        
class PaddleBall(Ball):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = BLUE
        self.outerColor = WHITE
        self.r = 10
        self.outerDraw = -1
        self.outerR = [2,2,5,5,7,7,7,5,5,2,2]
        
    def hit(self):
        self.outerDraw = len(self.outerR)
        
    def update(self):
        if self.outerDraw >= 0:
            self.outerDraw -= 1
        
    def draw(self):
        
        if self.outerDraw >= 0:
            pygame.draw.circle(screen, self.outerColor, (self.x, self.y), self.r + self.outerR[self.outerDraw])
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
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
        yoff = (height - self.balls[-1].y) * .50
        
        for ball in self.balls:
            ball.x -= xoff
            ball.y += yoff
            
        xoff = self.balls[-self.topCol-self.rows+1].x//2
        
        for ball in self.balls:
            ball.x -= xoff

#==========================================================================================================================
class BottomSquare(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.w = self.r
        self.h = self.r*10
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
#==========================================================================================================================        
class AwardSquare(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.w = self.r
        self.h = self.r*10
        self.color = RED
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))        
#==========================================================================================================================        
class BottomSquares(BottomSquare):
    
    def __init__(self, paddleBalls):
        super().__init__(0,0)
        self.squares = []
        
        for i in range(paddleBalls.topCol+paddleBalls.rows-1):
            self.squares.append(BottomSquare(paddleBalls.balls[-1-i].x-(self.r/2),height-self.h))
        
    def update(self):
        for square in self.squares:
            square.update()
            
    def draw(self):
        for square in self.squares:
            square.draw()
#==========================================================================================================================            
class AwardSquares(AwardSquare):
    
    def __init__(self, paddleBalls):
        super().__init__(0,0)
        self.squares = []
        self.color = RED
        
        for i in range(1,paddleBalls.topCol+paddleBalls.rows-1):
            self.squares.append(AwardSquare(paddleBalls.balls[-1-i].x + self.w/2,height-self.h))
            self.squares[-1].h -= 10
            self.squares[-1].color = COLORLIST[random.randint(0,2)]
            self.squares[-1].y += 10
            self.squares[-1].w = paddleBalls.offsetW - self.squares[-1].w
            
    def update(self):
        for square in self.squares:
            square.update()
            
    def draw(self):
        for square in self.squares:
            square.draw()        
#==========================================================================================================================
class CollisonHandler:
    
    
    def circleCircle(self, playerBall, paddleBall):
        x1 = playerBall.x
        y1 = playerBall.y
        x2 = paddleBall.x
        y2 = paddleBall.y
        
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        
        collides = dist < playerBall.r + paddleBall.r
        
        if collides:
            paddleBall.hit()
            playerBall.reflectOffPaddle(paddleBall)
        
        return collides
    
    
    def handleBallLists(self, paddleBalls, playerBalls):
        for paddleBall in paddleBalls.balls:
            for playerBall in playerBalls.balls:
                self.circleCircle(playerBall, paddleBall)
    
    def refelectBallAndSquare(self, bottomSquare, playerBall):
        bottomSquareRect = pygame.Rect(bottomSquare.x+bottomSquare.xv, bottomSquare.y+bottomSquare.yv, bottomSquare.w, bottomSquare.h)
        playerBallRect = pygame.Rect(playerBall.x-playerBall.r, playerBall.y-playerBall.r, playerBall.r*2, playerBall.r*2)
        collidesX = False
        collidesY = False
        
        normal = [0,1]
        
        if not bottomSquareRect.colliderect(playerBallRect):
            return
        
        playerBallRect.x -= playerBall.xv
        
        if not bottomSquareRect.colliderect(playerBallRect):
            collidesX = True
        
        playerBallRect.x += playerBall.xv
        playerBallRect.y -= playerBall.yv
        
        if not bottomSquareRect.colliderect(playerBallRect):
            collidesY = True
            
        if not collidesY and not collidesX:
            collidesY = True
            collidesX = True
            
        if collidesX and playerBall.xv > 0:
            normal = [-1,0]
        elif collidesX and playerBall.xv <= 0:
            normal = [1,0]
        
        if collidesY and playerBall.yv > 0:
            normal = [0,-1]
            
            
        
        speed = math.sqrt( (playerBall.x-(playerBall.xv+playerBall.x))**2 + (playerBall.y-(playerBall.yv+playerBall.y))**2)
        playerBall.xv, playerBall.yv = pygame.math.Vector2([playerBall.xv,playerBall.yv]).normalize().reflect(pygame.math.Vector2(normal)) * speed
        if abs(playerBall.xv) < .01:
            playerBall.xv += sign(playerBall.xv) * 1
        
                
    def handleBottomSquaresAndBall(self, bottomSquares, playerBalls):
        for playerBall in playerBalls.balls:
            for bottomSquare in bottomSquares.squares:
                self.refelectBallAndSquare(bottomSquare, playerBall)
                
        
#==========================================================================================================================            
class Game:
    
    def __init__(self):
        self.paddleBalls = PaddleBalls()
        self.playerBalls = PlayerBalls()
        self.bottomSquares = BottomSquares(self.paddleBalls)
        self.awardSquares = AwardSquares(self.paddleBalls)
        self.collisonHandler = CollisonHandler()
              
    def buttonEvent(self, direction, pressed):
        pass
    
    def mouseEvent(self, button, pressed, x, y):
        self.playerBalls.spawnBall(x, y, self.paddleBalls)
        
    def handleCollisons(self):
        self.collisonHandler.handleBallLists(self.paddleBalls, self.playerBalls)
        self.collisonHandler.handleBottomSquaresAndBall(self.bottomSquares, self.playerBalls)
        
    def update(self):
        self.handleCollisons()
        self.paddleBalls.update()
        self.playerBalls.update()
        self.bottomSquares.update()
        self.awardSquares.update()
    
    def draw(self):
        self.paddleBalls.draw()
        self.awardSquares.draw()
        self.playerBalls.draw()
        self.bottomSquares.draw()

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
        
        
        
        
