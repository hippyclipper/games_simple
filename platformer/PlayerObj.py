from gameObject import GameObject
from constants import *
import math
import pygame

#when yv down falling
#when yv up jumping
#when yv == 0 do x animations
#if moving do run in corrosponding dirrection
#if not moving then idle



class Player(GameObject):
    
    def __init__(self,level):
        
        super().__init__(level.playerSpawn[0],level.playerSpawn[1])
        self.color = GREEN
        self.g = 1
        self.w = 30
        self.h = 30
        self.a = 1
        self.grounded = False
        self.walled = False
        self.jumpVel = 20
        self.maxXVel = 8
        self.leftPress = False
        self.rightPress = False
        self.lastPress = ""
        
        self.jumpFilepath = "assests/VirtualGuy/Jump.png"
        self.jumpImage = pygame.image.load(self.jumpFilepath)
        self.jumpImageRight = pygame.transform.scale(self.jumpImage, (self.w, self.h))
        self.jumpImageLeft = pygame.transform.flip(self.jumpImageRight, True, False)
        
        self.fallFilepath = "assests/VirtualGuy/Fall.png"
        self.fallImage = pygame.image.load(self.fallFilepath)
        self.fallImageRight = pygame.transform.scale(self.fallImage, (self.w, self.h))
        self.fallImageLeft = pygame.transform.flip(self.fallImageRight, True, False)
        
        self.lastImage = self.jumpImageRight
        
        self.idleFilePath = None
        self.idleSheet = None
        self.idleSheetSize = None
        self.idleImages = []
        #self.spriteSheet.subsurface(pygame.Rect(self.ix+(image*self.pixelOffset), self.iy, self.iw, self.ih))
        
                        
    def movementPress(self, direction, pressed):     
        if direction == "right":
            self.rightPress = pressed
            self.lastPress = direction
        elif direction == "left":
            self.leftPress = pressed
            self.lastPress = direction
        elif direction in ["space", "up"] and pressed:
            self.jump()
                               
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.yv -= self.jumpVel
            
    def update(self):
        
        if self.rightPress and not self.leftPress:
            self.xv = min(self.maxXVel, self.xv+self.a)
        elif not self.rightPress and self.leftPress:
            self.xv = max(-self.maxXVel, self.xv-self.a)
        elif self.rightPress and self.leftPress:
            if self.lastPress == "right":
                self.xv = min(self.maxXVel, self.xv+self.a)
            else:
                self.xv = max(-self.maxXVel, self.xv-self.a)
        else:
            self.xv = 0            
        
        if not self.grounded:
            self.yv += self.g
            self.y += self.yv
        if not self.walled:    
            self.x += self.xv
                  
    def draw(self):
        if self.xv > 0 and self.yv == 0:
            #right on ground
            screen.blit(self.jumpImageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.jumpImageRight
        elif self.xv < 0 and self.yv == 0:
            #left on ground
            screen.blit(self.jumpImageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.jumpImageLeft
        elif self.xv == 0 and self.yv == 0:
            #idle
            screen.blit(self.lastImage, pygame.Rect(self.x, self.y, self.w, self.h ))
        elif self.yv > 0 and self.xv > 0:
            #falling right
            screen.blit(self.fallImageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.fallImageRight
        elif self.yv > 0 and self.xv < 0:
            #fall left
            screen.blit(self.fallImageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.fallImageLeft
        elif self.yv < 0 and self.xv < 0:
            #jump left
            screen.blit(self.jumpImageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.jumpImageLeft            
        elif self.yv < 0 and self.xv > 0:
            #jump right
            screen.blit(self.jumpImageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.jumpImageRight           
        elif self.yv > 0 and self.xv == 0:
            if self.lastPress == "right":
                screen.blit(self.fallImageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
                self.lastImage = self.fallImageRight
            else:
                screen.blit(self.fallImageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
                self.lastImage = self.fallImageLeft
        elif self.yv < 0 and self.xv == 0:
            if self.lastPress == "right":
                screen.blit(self.jumpImageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
                self.lastImage = self.jumpImageRight
            else:
                screen.blit(self.jumpImageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
                self.lastImage = self.jumpImageLeft          
