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
#font = pygame.font.SysFont('arial', 75)

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

def wrap(vector, offset):
    
    if offset+vector[0] > width:
        vector[0] = 0
    elif vector[0] < 0-offset:
        vector[0] = width
    
    if offset+vector[1] > height:
        vector[1] = 0
    elif vector[1] < 0-offset:
        vector[1] = height
        
def adjustMiddle(postion, middle, radius, dist):
    if -radius < postion-middle < radius:
        return postion + ([1,-1][random.randint(0,1)] * dist)
    else:
        return postion
    
class Astroid:
    
    def __init__(self,x,y, size = 3):
        velRange = 4-size
        self.location = [x, y]
        self.vel = [(.5+random.random()) * random.randint(-velRange,velRange),(.5+random.random()) * random.randint(-velRange,-velRange)]
        self.nodes = []
        self.points = 10
        self.deleteMe = False
        self.size = size
        self.color = (255,255,255)
        for x in range(self.points):
            scale = random.randint(10,20) * self.size
            rad = math.pi * 2 * (x/self.points)
            x1 = self.location[0] + math.cos(rad) * scale
            y1 = self.location[1] + math.sin(rad) * scale
            self.nodes.append([x1,y1, rad, scale])
            
    def handleCollison(self, line2start, line2end):
        
        for x in range(self.points-1):
            line1start = [self.nodes[x][0], self.nodes[x][1]]
            line1end = [self.nodes[x+1][0], self.nodes[x+1][1]]
            if contact(line1start, line1end, line2start, line2end):
                return True

        line1start = [self.nodes[0][0], self.nodes[0][1]]
        line1end = [self.nodes[-1][0], self.nodes[-1][1]]

        if contact(line1start, line1end, line2start, line2end):
            return True
        
        return False

        
    def update(self):
        
        wrap(self.location,0)
        
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
            pygame.draw.line(screen, self.color, first, last, 1)
            
            
        first = (self.nodes[0][0], self.nodes[0][1])
        last = (self.nodes[-1][0], self.nodes[-1][1])
        
        pygame.draw.line(screen, self.color, first, last, 1)


class Astroids:
    
    def __init__(self):
        self.astroids = []
        for x in range(6):
            randx = random.randint(0, width) 
            randy = random.randint(0, height)
            randx = adjustMiddle(randx, width//2, 100,200)
            randy = adjustMiddle(randy, height//2, 100,200)
            self.astroids.append(Astroid(randx, randy))
            
    def handleRespawn(self):
        for astroid in self.astroids:
            if pygame.Vector2(astroid.location).distance_to([width//2, height//2]) < 100:
                astroid.location[0] = width * 2
                astroid.location[1] = height * 2
            
    def checkCollisons(self, ship, hud):
        if len(self.astroids) == 0:
            hud.winGame()
        if ship.deathCounter == 1:
            self.handleRespawn()
                
        for bullet in ship.bullets:
            for astroid in self.astroids:
                if astroid.handleCollison(bullet.location, [bullet.location[0]+bullet.xv, bullet.location[1]+bullet.yv]):
                    astroid.deleteMe = True
                    bullet.deleteMe = True
                    hud.score += (4-astroid.size) * 10
                    break
          
        for astroid in self.astroids:
            if astroid.handleCollison(ship.tip, ship.backRight) or astroid.handleCollison(ship.tip, ship.backLeft) or astroid.handleCollison(ship.backRight, ship.backLeft):
                if not ship.hit:
                    hud.lives -= 1
                    hud.score = max(hud.score-100, 0)
                ship.die()
                
        
    def update(self):
        
        for astroid in self.astroids:
            astroid.update()
            if astroid.deleteMe:
                size = None
                numNew = None
                if astroid.size == 3:
                    numNew = 2
                    size = 2
                elif astroid.size == 2:
                    numNew = 2
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
        self.speed = 12
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
        
        wrap(self.location,0)

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
        self.rocketTip = [0,0]
        self.rocketBackLeft = [0,0]
        self.rocketBackRight = [0,0]
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
        self.hit = False
        self.flicker = 0
        self.deathCounter = 120
        self.deadShip = [[[0,0]]]
        
         
    def die(self):
        self.hit = True
        self.stopRocket()
        self.deadShip = [ [ [self.center[0]+10, self.center[1]+10],[self.center[0]-10, self.center[1]+5] ],
                          [ [self.center[0]-10, self.center[1]-10],[self.center[0]+5, self.center[1]+5] ],
                          [ [self.center[0]+5, self.center[1]-17],[self.center[0], self.center[1]] ],
                          [ [self.center[0]+12, self.center[1]-4],[self.center[0]-6, self.center[1]-7] ],
                          [ [self.center[0]-12, self.center[1]+4],[self.center[0]+6, self.center[1]-13] ] ]
 
#         self.deadShip = [ [ [10, 10],[-10, 5] ],
#                            [ [-10, -10],[5, 5] ],
#                            [ [5, -17],[0, 10] ],
#                            [ [12, -4],[-6, -7] ],
#                            [ [-12, 4],[6, -13] ] ]
              
    def calcRotation(self, vector, offset, scale):
        
        vector[0] = self.center[0] + (math.cos(self.rad+offset) * scale)
        vector[1] = self.center[1] + (math.sin(self.rad+offset) * scale)   
    
    def updateFlame(self):
        
        self.calcRotation(self.rocketTip, math.pi, 20)
        
        self.rocketBackLeft[0] = self.backLeft[0] - ((self.backLeft[0] - self.backRight[0]) * .2)
        self.rocketBackLeft[1] = self.backLeft[1] - ((self.backLeft[1] - self.backRight[1]) * .2)
        
        self.rocketBackRight[0] = self.backRight[0] - ((self.backRight[0] - self.backLeft[0]) * .2)
        self.rocketBackRight[1] = self.backRight[1] - ((self.backRight[1] - self.backLeft[1]) * .2)
        
        

    
    
    def update(self):
        
        wrap(self.center, 0)
        
        for bullet in self.bullets:
            bullet.update()
            if bullet.deleteMe:
                self.bullets.remove(bullet)
        
        
        self.updateDead()
        
        if self.deathCounter == 0:
            self.reset()
                
        if self.up and not self.hit:           
            self.flicker += 1
            self.acc[0] = math.cos(self.rad) * self.speed
            self.acc[1] = math.sin(self.rad) * self.speed           
        elif self.hit:
            self.acc = [0,0]
        
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
            
        if self.fire:
            self.fire = False
        
        self.calcRotation(self.tip, 0, 17)
        self.calcRotation(self.backLeft, math.pi * 2 * (5/8), 15) 
        self.calcRotation(self.backRight, math.pi * 2 * (3/8), 15) 
        
        self.updateFlame()
        
    
    def reset(self):
        self.center = [ width//2, height//2 ]
        self.rad = math.pi * 2 * .75
        self.vel = [0,0]
        self.acc = [0,0]
        self.hit = False
        self.fire = False
        self.left = False
        self.right = False
        self.up = False
        self.bullets = []
        self.deathCounter = 120
    
    def startRightTurn(self):

        self.right = True
        self.lastPress = "right"
    
    def startLeftTurn(self):
        self.left = True
        self.lastPress = "left"
        
    def fireGun(self):
        if self.hit: return
        self.fire = True
        self.bullets.append(Bullet(self.tip[:], self.rad))
        
    def startRocket(self):

        self.up = True
        self.acc[0] = math.cos(self.rad) * self.speed
        self.acc[1] = math.sin(self.rad) * self.speed
        
    def stopRocket(self):
        self.up = False
        self.acc = [0, 0]
        self.flicker = 0
    
    def updateDead(self):
        if self.hit:
            self.deathCounter -= 1
            for points in self.deadShip:
                for point in points:
                    point[0] += self.vel[0]
                    point[1] += self.vel[1]
                    
                    

    def draw(self):
        
        for bullet in self.bullets:
            bullet.draw()
            
        if self.hit:
            for points in self.deadShip:
                pygame.draw.line(screen, self.color, points[0], points[1], 2)
            return
        
        if self.up and self.flicker % 10 <= 5:
            pygame.draw.line(screen, self.color, self.rocketTip, self.rocketBackLeft, 2)
            pygame.draw.line(screen, self.color, self.rocketTip, self.rocketBackRight, 2)

        pygame.draw.line(screen, self.color, self.tip, self.backLeft, 2)
        pygame.draw.line(screen, self.color, self.tip, self.backRight, 2)
        pygame.draw.line(screen, self.color, self.backLeft, self.backRight, 2)
        

class Hud:
     
    def __init__(self):
        self.dummyShips = [Ship(), Ship(), Ship()]
        self.lives = 3
        self.score = 0
        self.color = (255,255,255)      
        self.font = pygame.font.SysFont('arial', 30)
        
        self.textScore = self.font.render(str(self.score),True,self.color)
        self.title = self.font.render("ASTROIDS",True,self.color)
        self.gameOverText = self.font.render("GAME OVER",True,self.color)
        self.youWon = self.font.render("YOU WON",True,self.color)
        
        self.startScreen = True
        self.inGame = False
        self.gameOver = False
        self.wonLevel = False
        
        self.titleLoc = self.title.get_rect(center = screen.get_rect().center)
        self.gameOverTextLoc = self.gameOverText.get_rect(center = screen.get_rect().center)
        self.youWonLoc = self.youWon.get_rect(center = screen.get_rect().center)
        
        
        for i,ship in enumerate(self.dummyShips):
            ship.center[0] = 25 + (i * 30)
            ship.center[1] = 60
            ship.update()
            
    def winGame(self):
        self.inGame = False
        self.wonLevel = True

            
    def hitSpace(self):
        if self.inGame:
            return
        elif self.startScreen:
            self.startScreen = False
            self.inGame = True
        elif self.gameOver:
            self.gameOver = False
            self.startScreen = True
        elif self.wonLevel:
            self.inGame = False
            self.startScreen = True
            self.wonLevel = False
        self.score = 0
        self.lives = 3
    
    def update(self):
        
        if self.lives == 0:
            self.lives = 3
            self.gameOver = True
            self.inGame = False
            
        self.textScore = self.font.render(str(self.score),True,self.color)
    
    def draw(self):
             
        if self.startScreen:
            screen.blit(self.title, [self.titleLoc[0], self.titleLoc[1]-50])
        if self.inGame:
            for x in range(self.lives):
                self.dummyShips[x].draw()
            screen.blit(self.textScore, [10,5])
        if self.gameOver:
            screen.blit(self.gameOverText, [self.gameOverTextLoc[0], self.gameOverTextLoc[1]-50])
        if self.wonLevel:
            screen.blit(self.youWon, [self.youWonLoc[0], self.youWonLoc[1]-50])
        
ship = Ship()
astroids = Astroids()
hud = Hud()

while not done:
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            if hud.startScreen:
                ship = Ship()
                astroids = Astroids()
            elif hud.inGame:
                ship.fireGun()
            hud.hitSpace()           
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

    hud.update()
    
    if hud.inGame:
    
           
        astroids.update()
        astroids.checkCollisons(ship, hud)  
        ship.update()
          
        
        astroids.draw()
        ship.draw()
      
    hud.draw()
                
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
pygame.display.quit()
pygame.quit()    