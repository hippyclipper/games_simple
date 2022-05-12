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

class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0
        self.yv = 0
        self.numSquarePerRow = 21
        self.w = width//self.numSquarePerRow
        self.h = self.w
        self.color = WHITE
        
    def update(self):
        pass
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))


class Square(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = BACKGROUND

class PlayerSquare(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = WHITE
        
        
class Player(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.x = (self.numSquarePerRow//2)*self.w
        self.y = (self.numSquarePerRow//2)*self.h
        self.stepW = self.w
        self.stepH = self.h
        self.frameWaitMax = 6
        self.frameWait = self.frameWaitMax
        self.playerTiles = [PlayerSquare(self.x, self.y)]
        self.addNew = False
        
    def handleButtonPress(self, direction):
        
        if direction == "up":
            self.playerTiles[0].yv = -1
            self.playerTiles[0].xv = 0
        elif direction == "down":
            self.playerTiles[0].yv = 1
            self.playerTiles[0].xv = 0
        elif direction == "left":
            self.playerTiles[0].yv = 0
            self.playerTiles[0].xv = -1
        elif direction == "right":
            self.playerTiles[0].yv = 0
            self.playerTiles[0].xv = 1
        elif direction == "space":
            self.addNew = True
            
    
    
    
    def checkSelfIntersect(self):
        for tile1 in self.playerTiles:
            for tile2 in self.playerTiles:
                if tile1 == tile2:
                    continue
                tile1Rect = pygame.Rect(tile1.x, tile1.y, tile1.w, tile1.h)
                tile2Rect = pygame.Rect(tile2.x+2, tile2.y+2, tile2.w-4, tile2.h-4)
                if tile1Rect.colliderect(tile2Rect):
                    print("collide self")
    
    
    def update(self):
        
        if self.frameWait > 0:
            self.frameWait -= 1
            return
        else:
            self.frameWait = self.frameWaitMax
            
            
        lastX = self.playerTiles[0].x
        lastY = self.playerTiles[0].y
        self.playerTiles[0].x += self.playerTiles[0].xv*self.stepW
        self.playerTiles[0].y += self.playerTiles[0].yv*self.stepH
        storeX = lastX
        storeY = lastY
        
        for x in range(1,len(self.playerTiles)):
            storeX = self.playerTiles[x].x
            storeY = self.playerTiles[x].y 
            self.playerTiles[x].x = lastX
            self.playerTiles[x].y = lastY
            lastX = storeX
            lastY = storeY

            
        if self.addNew:
            self.playerTiles.append(PlayerSquare(storeX, storeY))
            self.addNew = False
            
    def draw(self):
        for tiles in self.playerTiles:
            tiles.draw()
    
class Game:
    
    def __init__(self):
        self.player = Player()
               
    def handleCollisions(self):
        self.player.checkSelfIntersect()
    
    def buttonEvent(self, direction, pressed):
        self.player.handleButtonPress(direction)
        
    def update(self):
        self.handleCollisions()
        self.player.update()
        
    def draw(self):
        self.player.draw()

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
            
            
    game.update()
    game.draw()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#=============================================================
pygame.display.quit()
pygame.quit()    
