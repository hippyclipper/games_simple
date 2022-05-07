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


def circleLineCollison(lineStart, lineEnd, circleX, circleY, circleR):
    pass

#==========================================================================================================================
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
#==========================================================================================================================
        
class ScoreBoard(GameObject):
    
    def __init__(self):
        
        super().__init__(0,0)
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.SysFont('arial', 50)
        self.textScore1 = self.font.render(str(self.score1),True,self.color)
        self.textScore2 = self.font.render(str(self.score2),True,self.color)
        
        self.score1loc = self.textScore1.get_rect(center = screen.get_rect().center)
        self.score2loc = self.score1loc[:]
        
        self.score1loc[0] += width//4
        self.score2loc[0] -= width//4
        
        self.score1loc[1] = 10
        self.score2loc[1] = 10
        
            
    def update(self):
        self.textScore1 = self.font.render(str(self.score1),True,self.color)
        self.textScore2 = self.font.render(str(self.score2),True,self.color)
        
    def draw(self):
        screen.blit(self.textScore1, self.score1loc)
        screen.blit(self.textScore2, self.score2loc)

        
class Paddle(GameObject):
    
    def __init__(self,x,y):
        self.widthScale = 10
        self.paddleV = 10
        super().__init__(x,y)
        self.y -= self.r*self.widthScale//2
        self.up = False
        self.down = False
        self.offset = 0
        
    def vScale(self, bPlace, pRange):    
        return 1-(bPlace/pRange)
    
    def handleCollison(self, ball):
        
        ballRect = pygame.Rect(ball.x-ball.r, ball.y-ball.r, ball.r*2, ball.r*2)
        paddleRect = pygame.Rect(self.x, self.y, self.r, self.r*self.widthScale )
        if ballRect.colliderect(paddleRect):
            paddleBottom = (self.r*self.widthScale) + self.y + ball.r
            paddleTop = self.y - ball.r
            pRange = paddleBottom - paddleTop
            bPlace = paddleBottom - ball.y 
            vectorScale = self.vScale(bPlace, pRange)
            down = math.pi/2
            up = math.pi+math.pi/2
            vec = self.offset + math.pi + down + abs(up-down)*vectorScale
            ball.xv, ball.yv = ball.calcVector(vec, ball.maxVel)

            

        
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
#==========================================================================================================================        
class LeftPaddle(Paddle):
    def __init__(self,x,y):
        super().__init__(x,y)
        
        
    def handleEvent(self,direction,pressed):
        
        if direction == "down" and pressed:
            self.moveDown()
        elif direction =="up" and pressed:
            self.moveUp()
        elif direction in ["up", "down"] and not pressed:
            self.stop(direction)                   
#==========================================================================================================================        
class RightPaddle(Paddle):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x -= self.r
        self.offset = math.pi
        
    def vScale(self, bPlace, pRange):    
        return bPlace/pRange
        
#==========================================================================================================================    
class Ball(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.maxVel = 5
        self.xv, self.yv = self.calcVector(random.uniform(-.25*math.pi, .25*math.pi)+[0,math.pi][random.randint(0,1)], self.maxVel)
        #self.xv, self.yv = self.calcVector(math.pi+.002, self.maxVel)
        self.waitFrames = 30
        self.score = ""
        
    def reset(self, score):
        self.score = score
        self.x = width//2
        self.y = height//2
        self.xv, self.yv = self.calcVector(random.uniform(-.25*math.pi, .25*math.pi)+[0,math.pi][random.randint(0,1)], self.maxVel)
        self.waitFrames = 30
        
    def update(self):
        
        if self.waitFrames > 0:
            self.waitFrames -= 1
            return
        
        if self.y < 0 + self.r:
            self.xv, self.yv = pygame.math.Vector2([self.xv,self.yv]).normalize().reflect(pygame.math.Vector2([0,1])) * self.maxVel
        elif self.y > height - self.r:
            self.xv, self.yv = pygame.math.Vector2([self.xv,self.yv]).normalize().reflect(pygame.math.Vector2([0,-1])) * self.maxVel
            
        if self.x > width+self.r:
            self.reset("right")
            return
        elif self.x < 0-self.r:
            self.reset("left")
            return
            
        self.x += self.xv
        self.y += self.yv
#==========================================================================================================================        
class MidLine(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.x -= self.r//2
        self.numSquares = 20
        self.widthScale = 3
        self.color = WHITE
        
    def draw(self):
        for x in range(self.numSquares):
            pygame.draw.rect(screen, self.color, pygame.Rect(self.x, x*50, self.r, self.r*self.widthScale ))
#==========================================================================================================================              
class Game:
    
    def __init__(self):
        self.paddleLeft = LeftPaddle(0, height//2)
        self.scoreBoard = ScoreBoard()
        self.paddleRight = RightPaddle(width, height//2)
        self.ball = Ball(width//2, height//2)
        self.midLine = MidLine(width//2, 0)
        
    def buttonEvent(self, direction, pressed):
        self.paddleLeft.handleEvent(direction, pressed)
        
    def handleCollisons(self):
        
        if self.ball.score == "right":
            self.scoreBoard.score1 += 1
            self.ball.score = ""
        elif self.ball.score == "left":
            self.scoreBoard.score2 += 1
            self.ball.score = ""
            
        self.paddleLeft.handleCollison(self.ball)
        self.paddleRight.handleCollison(self.ball)
        #paddleLeft and ball
        #scoreboard and ball 
        
    def update(self):
        self.handleCollisons()
        self.paddleLeft.update()
        self.paddleRight.update()
        self.ball.update()
        self.scoreBoard.update()
    
    def draw(self):
        self.midLine.draw()
        self.paddleLeft.draw()
        self.paddleRight.draw()
        self.ball.draw()
        self.scoreBoard.draw()

game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            pass
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            game.buttonEvent("up", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            game.buttonEvent("up", False)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            game.buttonEvent("down", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            game.buttonEvent("down", False)
                   
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#==========================================================================================================================
pygame.display.quit()
pygame.quit()    
