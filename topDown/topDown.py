import pygame
import random
import math
from perlin_noise import PerlinNoise
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

# self.idleFilePath = "assests/VirtualGuy/Idle(32x32).png"
# self.idleSheet = pygame.image.load(self.idleFilePath)
# self.idleframeNum = 10
# self.idleSheetSize = self.idleSheet.get_size()
# self.idleImages = []
# for x in range(self.idleframeNum):
# self.idleImages.append(self.idleSheet.subsurface(pygame.Rect(5+(x*22)+(x*10),6,22,26)))
# self.fallFilepath = "assests/VirtualGuy/Fall.png"
# self.fallImage = pygame.image.load(self.fallFilepath)
# self.fallImage = self.fallImage.subsurface(pygame.Rect(5,6,23,26)) 
# self.fallImage = pygame.transform.smoothscale(self.fallImage, (self.w, self.h)) 
# self.fallImageLeft = pygame.transform.flip(self.fallImageRight, True, False)
# screen.blit(self.cloudImage, pygame.Rect(self.x, self.y, self.w, self.h ))
# pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
# self.font = pygame.font.SysFont('arial', 80)
# self.textScore = self.font.render(str(self.scoreInt),True,self.color)
# self.textScoreLocation = self.textScore.get_rect(center = screen.get_rect().center)
# rect2 = pygame.Rect(square.x, square.y, square.w, square.h )
# rect2.colliderect(rect1)
# noise = PerlinNoise(octaves=2, seed=randseed)
# value = noise([x, y, z])

#todo
#chunks 250x250
#grass (everywhere)
#camera movement (world movement)
#flowers (perlin noise patches)
#rock (collision)
#trees (collison, perlin noise)
#lakes (boarders)
#animal/creater


# https://pixelmochii.itch.io/mochii-plains
# https://opengameart.org/content/the-field-of-the-floating-islands

#======================================================================

class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0 
        self.yv = 0
        self.r = 10
        self.w = 15
        self.h = 15
        self.tileW = self.w
        self.tileH = self.h
        self.xw = 0
        self.yw = 0
        self.color = WHITE
        self.chunkSize = 250
        
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

#======================================================================

class ImageGallery(GameObject):
    
    def __init__(self):
        super().__init__(0,0)       

#======================================================================

class Tile(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        
    def offScreen(self):
        if self.x+self.w < 0:
            return True
        elif self.x > width:
            return True
        elif self.y+self.h < 0:
            return True
        elif self.y > height:
            return True
        return False
        
    def draw(self):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
            
#======================================================================

class Grass(Tile):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = GREEN
 
#======================================================================
 
class Water(Tile):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        self.color = BLUE
        
#======================================================================
 
class WorldTiles(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.tiles = []
        self.scrollSpeed = 3
        for x in range(self.chunkSize):
            for y in range(self.chunkSize):
                self.createTile(x,y)
                    
    def createTile(self,x,y):
            if random.randint(0,1000) < 990:
                self.tiles.append(Grass(x*self.tileW, y*self.tileH))
            else:
                self.tiles.append(Water(x*self.tileW, y*self.tileH))
                    
                    
    def moveWorld(self, pressedKeys):
        
        for tile in self.tiles:
            if "left" in pressedKeys.pressed :
                tile.move(self.scrollSpeed, 0)
            if "right" in pressedKeys.pressed:
                tile.move(-self.scrollSpeed, 0)
            if "up" in pressedKeys.pressed:
                tile.move(0,self.scrollSpeed)
            if "down" in pressedKeys.pressed:
                tile.move(0,-self.scrollSpeed)
                     
    def draw(self):
        for tile in self.tiles:
            if tile.offScreen():
                continue
            tile.draw()

#======================================================================

class Player(GameObject):
    def __init__(self):
        super().__init__(width//2, height//2)
        self.color = RED
    
#======================================================================  
        
        
class PressedKeys:
    
    def __init__(self):
        self.pressed = set({})
        
    def handlePress(self, direction, pressed):
        if pressed:
            self.pressed.add(direction)
        else:
            self.pressed.remove(direction)
        
class Game:
    
    def __init__(self):
        self.player = Player()
        self.worldTiles = WorldTiles()
        self.pressedKeys = PressedKeys()
        
    def buttonEvent(self, direction, pressed):
        self.pressedKeys.handlePress(direction, pressed)
        
    def handleCollisons(self):
        self.worldTiles.moveWorld(self.pressedKeys)
        
    def update(self):
        self.handleCollisons()
        self.player.update()
        self.worldTiles.update()
    
    def draw(self):
        self.worldTiles.draw()
        self.player.draw()

        
#======================================================================
        
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
            game.buttonEvent("left", False)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", False)
            
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
        
        
        
        
