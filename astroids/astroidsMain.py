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
COLORLIST = [RED, GREEN, BLUE]
done = False

class Bullet:
    
    def __init__(self, point, rad):
        
        self.location = point
        self.r = 3
        self.velRad = rad
        self.speed = 5
        self.color = (255,255,255)
        self.xv = math.cos(rad) * self.speed 
        self.yv = math.sin(rad) * self.speed 
        
        
        
    def update(self):
        self.location[0] += self.xv
        self.location[1] += self.yv
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.location, self.r)
        



class Ship:
    
    def __init__(self):
        self.center = [ width//2, height//2 ]
        self.tip = [0,0]
        self.backLeft = [0,0]
        self.backRight = [0,0]
        self.scale = 10
        self.rad = 0
        self.r = 2
        self.color = (255,255,255)
        self.fire = False
        self.left = False
        self.right = False
        self.up = False
        self.lastPress = ""
        self.bullets = []
        
      
    def calcRotation(self, vector, offset, scale):
        
        vector[0] = self.center[0] + (math.cos(self.rad+offset) * scale)
        vector[1] = self.center[1] + (math.sin(self.rad+offset) * scale)   
      
    def update(self):

        if (self.left and not self.right):
            self.rad -= .1
        if (not self.left and self.right):
            self.rad += .1
        
        self.calcRotation(self.tip, math.pi * 2 * .75, 17)
        self.calcRotation(self.backLeft, math.pi * 2 * (1/8), 15) #G
        self.calcRotation(self.backRight, math.pi * 2 * (3/8), 15) #B
        for bullet in self.bullets:
            bullet.update()
        
    def startRightTurn(self):
        self.right = True
        self.lastPress = "right"
    
    def startLeftTurn(self):
        self.left = True
        self.lastPress = "left"
        
    def fireGun(self):
        self.fire = True
        self.bullets.append(Bullet(self.tip[:], (math.pi * 2 * .75)+self.rad))
        
    def startRocket(self):
        self.up = True

        
        
        
    def draw(self):
        
        if self.up:
            pygame.draw.circle(screen, RED, self.center, 2)
        
        if self.fire:
            pygame.draw.circle(screen, self.color, self.center, 2)
            self.fire = False
        pygame.draw.circle(screen, RED, self.tip, self.r)
        pygame.draw.circle(screen, GREEN, self.backLeft, self.r)
        pygame.draw.circle(screen, GREEN, self.backRight, self.r)
        for bullet in self.bullets:
            bullet.draw()

        
        
        
        #pygame.draw.line(screen, GREEN, (self.x1, self.y1), (self.x2, self.y2), 1)
        
ship = Ship()


while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            ship.fireGun()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            ship.startLeftTurn()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            ship.startRightTurn()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            ship.startRocket()
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            ship.left = False
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            ship.right = False
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            ship.up = False

        
    ship.update()        
    ship.draw()      
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
pygame.display.quit()
pygame.quit()    