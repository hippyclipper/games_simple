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

class PlayerSquare(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = RED
        
class Tiles(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.tiles = []
        for x in range(self.numSquarePerRow):
            self.tiles.append([])
            for y in range(self.numSquarePerRow):
                self.tiles[x].append(Square(self.w*x, self.h*y))

    def draw(self):
        for row in self.tiles:
            for tile in row:
                tile.draw()


class Player(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.x = (self.numSquarePerRow//2)*self.w
        self.y = (self.numSquarePerRow//2)*self.h
        self.step = self.w
        self.playerTiles = [PlayerSquare(self.x, self.y)]
            
    def update(self):
        pass
    
    def draw(self):
        for tiles in self.playerTiles:
            tiles.draw()
    


class Game:
    
    def __init__(self):
        self.tiles = Tiles()
        self.player = Player()
    def update(self):
        self.player.update()
        self.tiles.update()
    def draw(self):
        self.tiles.draw()
        self.player.draw()

game = Game()

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True           
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:           
            pass     
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            pass
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            pass      
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            pass
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
