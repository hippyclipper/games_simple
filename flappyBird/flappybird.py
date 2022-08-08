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
# self.fallImageLeft = pygame.transform.flip(self.fallImageRight, True, False)

#TODO
#bird animations
#   3 frames/wing flap/tilt based on yv
#score

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
        self.r = self.r*2
        self.frameCounter = 0
        self.frameJump = .2
        self.birdFrames = []
        self.jumpV  = 18  
        self.dead = False
        self.grounded = False
        self.color = RED
        self.birdFilePath = "./assets/Bird/Bird_spritesheet.png"
        self.birdImage = pygame.image.load(self.birdFilePath)
        #birdspritwidth = 482 startingXoffset = 19 startingYoffset = 100 birdheight = 315
        self.birdFrames.append(self.birdImage.subsurface(pygame.Rect(1041,98,482,315)))
        self.birdFrames.append(self.birdImage.subsurface(pygame.Rect(1041,610,482,315)))
        self.birdFrames.append(self.birdImage.subsurface(pygame.Rect(17,610 ,482,315)))
        

        for i,frame in enumerate(self.birdFrames):
            self.birdFrames[i] = pygame.transform.smoothscale(frame, (self.r*2*1.53, self.r*2))
        
        
        
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
        self.frameCounter += self.frameJump
        self.yv += self.g
        self.y += self.yv

    def rotateBird(self, image):
        
        angle = (self.yv/self.jumpV)*-30
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (self.x, self.y)).center)

        return rotated_image, new_rect

    def draw(self):
        drawImage, drawRect = self.rotateBird(self.birdFrames[int(self.frameCounter)%len(self.birdFrames)])
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        screen.blit(drawImage, pygame.Rect(drawRect.x, drawRect.y, self.r*2, self.r*2 ))
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

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
        self.w = 120
        self.h = h
        self.xv = -2
        self.topPipe = topPipe
        self.color = BLUE
        self.buffer = 1.4
        
        self.imageW = self.w
        self.imageH = height
        

        self.pipeFilePath = "./assets/Background/top_pipe-sheet0.png"
        self.pipeImage = pygame.image.load(self.pipeFilePath)        
        self.pipeImage = pygame.transform.smoothscale(self.pipeImage, (self.imageW , self.imageH ))
             
    def update(self):
        self.x += self.xv
        
    def stop(self):
        self.xv = 0
        
    def draw(self):
        
        if not self.topPipe:
            #pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
            screen.blit(self.pipeImage, pygame.Rect(self.x, self.y, self.imageW, self.imageH ))
            #pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
            
        else:
            #pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.w, self.h ))
            screen.blit(self.pipeImage, pygame.Rect(self.x, self.y-height+self.h , self.imageW, self.imageH ))

class Pipes(GameObject):
    
    def __init__(self,ground):
        super().__init__(width,0)
        self.pipes = []
        self.gapSize = 225
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
        hitboxScaleX = .7
        hitboxDifY = 20        
        rect2W = rect2.w
        rect2H = rect2.h
        rect2X = rect2.x
        rect2Y = rect2.y
        rect2.w = rect2W*hitboxScaleX
        rect2.h = rect2H-hitboxDifY
        rect2.x += (rect2W-rect2.w)//2
        if not square.topPipe:
            rect2.y += (rect2H-rect2.h)//2
        else:
            rect2.y += hitboxDifY//2
        #pygame.draw.rect(screen, self.color, rect2)
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



class Score(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        self.scoreInt = 0
        
        
    def getScore(self):
        return str(self.scoreInt)


   
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
        
        
        
        