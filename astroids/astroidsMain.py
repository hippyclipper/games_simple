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

def contact(line1start, line1end, line2start, line2end):
    x1 = line1start[0]
    y1 = line1start[1]
    
    x2 = line1end[0]
    y2 = line1end[1]
    
    x3 = line2start[0]
    y3 = line2start[1]
    
    x4 = line2end[0]
    y4 = line2end[1]
    
    D = ((x1 - x2) * (y3-y4)) - ((y1 - y2) * (x3 - x4))
    
    if D == 0:
        return False
    
    t = (((x1-x3) * (y3-y4)) - ((y1-y3) * (x3-x4))) / D
    u = (((x1-x3) * (y1-y2)) - ((y1-y3) * (x1-x2))) / D
    
    if not (0 <= t <= 1 and 0 <= u <= 1):
        return False
    
    return True

def wrap(vector):
    
    if vector[0] > width:
        vector[0] = 0
    elif vector[0] < 0:
        vector[0] = width
    
    if vector[1] > height:
        vector[1] = 0
    elif vector[1] < 0:
        vector[1] = height    

class Astroid:
    
    def __init__(self,x,y, size = 3):
        velRange = 4-size
        self.location = [x, y]
        self.vel = [random.random() * random.randint(-velRange,velRange),random.random() * random.randint(-velRange,-velRange)]
        self.nodes = []
        self.points = 10
        self.deleteMe = False
        self.size = size
        
        for x in range(self.points):
            scale = random.randint(10,20) * self.size
            rad = math.pi * 2 * (x/self.points)
            x1 = self.location[0] + math.cos(rad) * scale
            y1 = self.location[1] + math.sin(rad) * scale
            self.nodes.append([x1,y1, rad, scale])
            
    def handleBulletCollison(self, bullet):
        
        line2start = bullet.location
        line2end = [bullet.location[0]+bullet.xv, bullet.location[1]+bullet.yv]
        
        for x in range(self.points-1):
            line1start = [self.nodes[x][0], self.nodes[x][1]]
            line1end = [self.nodes[x+1][0], self.nodes[x+1][1]]
            if contact(line1start, line1end, line2start, line2end):
                bullet.deleteMe = True
                self.deleteMe = True

        line1start = [self.nodes[0][0], self.nodes[0][1]]
        line1end = [self.nodes[-1][0], self.nodes[-1][1]]

        if contact(line1start, line1end, line2start, line2end):
                bullet.deleteMe = True
                self.deleteMe = True

            
    def update(self):
        
        wrap(self.location)
        
        self.location[0] += self.vel[0]
        self.location[1] += self.vel[1]
        
        for node in self.nodes:
            node[2] += .01
                        
            node[0] = self.location[0] + math.cos(node[2]) * node[3]
            node[1] = self.location[1] + math.sin(node[2]) * node[3]
            
            node[0] += self.vel[0]
            node[1] += self.vel[1]
    
    def draw(self):
        for x in range(self.points-1):
            first = [self.nodes[x][0], self.nodes[x][1]]
            last = [self.nodes[x+1][0], self.nodes[x+1][1]]
            pygame.draw.line(screen, GREEN, first, last, 1)
            #pygame.draw.circle(screen, GREEN, self.nodes[x], 3)
            
        first = (self.nodes[0][0], self.nodes[0][1])
        last = (self.nodes[-1][0], self.nodes[-1][1])
        
        pygame.draw.line(screen, GREEN, first, last, 1)
        
class Astroids:
    
    def __init__(self):
        self.astroids = []
        for x in range(6):
            randx = random.randint(0, width) 
            randy = random.randint(0, height) 
            self.astroids.append(Astroid(randx, randy))        
            
    def checkCollisons(self, ship):
        for bullet in ship.bullets:
            for astroid in self.astroids:
                astroid.handleBulletCollison(bullet)
    
    def update(self):       
        for astroid in self.astroids:
            astroid.update()
            if astroid.deleteMe:
                size = None
                numNew = None
                if astroid.size == 3:
                    numNew = 3
                    size = 2
                elif astroid.size == 2:
                    numNew = 4
                    size = 1
                else:
                    numNew = 0
                    size = 1
                
                for x in range(numNew):
                    self.astroids.append(Astroid(astroid.location[0], astroid.location[1], size))                    
                self.astroids.remove(astroid)
                
    def draw(self):
        for x in self.astroids:
            x.draw()



class Bullet:
    
    def __init__(self, point, rad):
        
        self.location = point
        self.start = point[:]
        self.r = 3
        self.velRad = rad
        self.speed = 9
        self.color = (255,255,255)
        self.xv = math.cos(rad) * self.speed 
        self.yv = math.sin(rad) * self.speed
        self.deleteMe = False
        self.maxDis = 500
        self.travled = 0
                
    def update(self):
        self.location[0] += self.xv 
        self.location[1] += self.yv 
        
        self.travled += abs(self.xv) + abs(self.yv)
        
        wrap(self.location)

        if self.travled > self.maxDis:
            self.deleteMe = True
        
    def draw(self):
        pygame.draw.circle(screen, self.color, self.location, self.r)
  
  
class Ship:
    
    def __init__(self):
        self.center = [ width//2, height//2 ]
        self.tip = [0,0]
        self.backLeft = [0,0]
        self.backRight = [0,0]
        self.vel = [0,0]
        self.acc = [0,0]
        self.scale = 10
        self.rad = math.pi * 2 * .75
        self.r = 2
        self.speed = .1
        self.color = (255,255,255)
        self.fire = False
        self.left = False
        self.right = False
        self.up = False
        self.lastPress = ""
        self.bullets = []
        self.friction = .995
              
    def calcRotation(self, vector, offset, scale):
        
        vector[0] = self.center[0] + (math.cos(self.rad+offset) * scale)
        vector[1] = self.center[1] + (math.sin(self.rad+offset) * scale)   
      
    def update(self):
        
        wrap(self.center)
                
        if self.up:
            self.acc[0] = math.cos(self.rad) * self.speed
            self.acc[1] = math.sin(self.rad) * self.speed
        
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        
        self.vel[0] *= self.friction
        self.vel[1] *= self.friction       
        
        self.center[0] += self.vel[0]
        self.center[1] += self.vel[1]

        if (self.left and not self.right):
            self.rad -= .1
        if (not self.left and self.right):
            self.rad += .1
        
        self.calcRotation(self.tip, 0, 17)
        self.calcRotation(self.backLeft, math.pi * 2 * (5/8), 15) #G
        self.calcRotation(self.backRight, math.pi * 2 * (3/8), 15) #B
        
        for bullet in self.bullets:
            bullet.update()
            if bullet.deleteMe:
                self.bullets.remove(bullet)
        
    def startRightTurn(self):
        self.right = True
        self.lastPress = "right"
    
    def startLeftTurn(self):
        self.left = True
        self.lastPress = "left"
        
    def fireGun(self):
        self.fire = True
        self.bullets.append(Bullet(self.tip[:], self.rad))
        
    def startRocket(self):
        self.up = True
        self.acc[0] = math.cos(self.rad) * self.speed
        self.acc[1] = math.sin(self.rad) * self.speed
        
    def stopRocket(self):
        self.up = False
        self.acc = [0, 0]

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




ship = Ship()
astroids = Astroids()

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
            ship.stopRocket()
    
    astroids.checkCollisons(ship)
    
    astroids.update()
    astroids.draw()
    
    ship.update()        
    ship.draw()      
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
pygame.display.quit()
pygame.quit()    