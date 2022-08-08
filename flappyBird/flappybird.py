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
# self.fallImageRight = self.fallImage 
# self.fallImageLeft = pygame.transform.flip(self.fallImageRight, True, False)



class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0 
        self.yv = 0
        self.r = 10
        self.color = WHITE
        self.g = 1
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)


class Bird(GameObject):
    
    def __init__(self):
        super().__init__(width//4, height//2)
        self.jumpV  = 18  
        self.dead = False
        self.grounded = False
        self.color = RED
        
    def jump(self):
        if not self.dead:
            self.yv = -self.jumpV
        
    def die(self):
        self.dead = True
        self.yv = max(0,self.yv)
        
    def handlePress(self, direction, pressed):
        if direction == "space" and pressed:
            self.jump()
            
    def update(self):
        self.yv += self.g
        self.y += self.yv


class Background(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.w = width
        self.h = height
        self.backFilePath = "./assets/Background/background-sheet0.png"
        self.backImage = pygame.image.load(self.backFilePath)        
        self.backImage = pygame.transform.scale(self.backImage, (self.w, self.h))
        
    def draw(self):
        screen.blit(self.backImage, pygame.Rect(self.x, self.y, self.w, self.h ))
        
class Ground(GameObject):

    def __init__(self):
        self.h = 50
        super().__init__(0,height-self.h)
        self.w = width
        self.groundFilePath = "./assets/Background/ground-sheet0.png"
        self.groundImage = pygame.image.load(self.groundFilePath)        
        self.groundImage = pygame.transform.smoothscale(self.groundImage, (self.w, self.h))
        self.xv = -2
        self.stopMoving = False
    
    def stop(self):
        self.stopMoving = True
    
    def update(self):
        if self.stopMoving:
            return
        self.x += self.xv
        if self.x == -self.w:
            self.x = 0

    
    def draw(self):
        screen.blit(self.groundImage, pygame.Rect(self.x, self.y, self.w, self.h ))
        screen.blit(self.groundImage, pygame.Rect(self.x+self.w, self.y, self.w, self.h ))
        
class Pipe(GameObject):
    
    def __init__(self,x,y,h,topPipe):
        super().__init__(x,y)
        self.w = 100
        self.h = h
        self.xv = -2
        self.topPipe = topPipe
        self.color = BLUE

        self.pipeFilePath = "./assets/Background/top_pipe-sheet0.png"
        self.pipeImage = pygame.image.load(self.pipeFilePath)        
        self.pipeImage = pygame.transform.smoothscale(self.pipeImage, (self.w, height))
               
    def update(self):
        self.x += self.xv
        
    def stop(self):
        self.xv = 0
        
    def draw(self):
        
        if not self.topPipe:
            screen.blit(self.pipeImage, pygame.Rect(self.x, self.y, self.w, self.h ))
        else:
            screen.blit(self.pipeImage, pygame.Rect(self.x, self.y-height+self.h , self.w, self.h ))

class Pipes(GameObject):
    
    def __init__(self,ground):
        super().__init__(width,0)
        self.pipes = []
        self.gapSize = 220
        self.waitTime = 140
        self.counter = self.waitTime
        self.border = 20
        self.groundHeight = ground.h
        self.keepSpawning = True
        
        
        
        self.addPipe()

    def stop(self):
        self.keepSpawning = False
        for pipe in self.pipes:
            pipe.stop()
    
    def addPipe(self):
        if not self.keepSpawning:
            return
        randY = random.randint(self.border, height - self.gapSize - self.border - self.groundHeight)
        pipe1 = Pipe(width, 0, randY,True)
        pipe2 = Pipe(width, self.gapSize+randY, height-(self.gapSize+randY),False )
        self.pipes.append(pipe1)
        self.pipes.append(pipe2)
        
    def update(self):
        self.counter -= 1
        if self.counter == 0:
            self.addPipe()
            self.counter = self.waitTime
        for pipe in self.pipes:
            pipe.update()
            
    def draw(self):
        for pipe in self.pipes:
            pipe.draw()



class Collisions(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
    
    def playerCollides(self, player, square):
        rect1 = pygame.Rect(player.x-player.r, player.y-player.r, player.r*2, player.r*2)
        rect2 = pygame.Rect(square.x, square.y, square.w, square.h )
        return rect2.colliderect(rect1)
    
    
    def handleBirdAndPipes(self, bird, pipes, ground):
   
        for pipe in pipes.pipes:
            if self.playerCollides(bird,pipe):
                bird.die()
                
        if bird.y+bird.r > ground.y:
            bird.die()
            bird.y = ground.y - bird.r
            bird.grounded = True
            bird.yv = 0            
        
        if bird.dead:
            pipes.stop()
            ground.stop()
   
   
class Game:
    
    def __init__(self):
        self.bird = Bird()
        self.ground = Ground()
        self.pipes = Pipes(self.ground)
        self.collisions = Collisions()
        self.background = Background()
        self.restartTimer = 0
        self.deathResetTime = 100
        
      
    def reset(self):
        self.bird = Bird()
        self.ground = Ground()
        self.pipes = Pipes(self.ground)
        self.collisions = Collisions()
        self.restartTimer = 0
          
    def buttonEvent(self, direction, pressed):
        self.bird.handlePress(direction, pressed)
        
    def handleCollisons(self):
        self.collisions.handleBirdAndPipes(self.bird, self.pipes, self.ground)
    
    
    def checkBirdDeath(self):
        if self.bird.dead:
            self.restartTimer += 1
            if self.restartTimer == self.deathResetTime:
                self.reset()
    
    def update(self):
        self.checkBirdDeath()
        self.handleCollisons()
        
        self.background.update()
        self.bird.update()
        self.pipes.update()
        self.ground.update()
    
    def draw(self):
        self.background.draw()
        self.pipes.draw()
        self.ground.draw()
        self.bird.draw()

        
        
        
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
                   
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#==========================================================================================================================
pygame.display.quit()
pygame.quit()    
        
        
        
        