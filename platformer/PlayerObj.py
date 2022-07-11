from gameObject import GameObject
from constants import *
import math
import pygame


class Player(GameObject):
    
    def __init__(self,level):
        
        super().__init__(level.playerSpawn[0],level.playerSpawn[1])
        self.color = GREEN
        self.g = 1
        self.w = 30
        self.h = 30
        self.grounded = False
        self.walled = False
        self.jumpVel = 20
        self.maxXVel = 8
        self.leftPress = False
        self.rightPress = False
        self.lastPress = ""
        self.genFilepath = "assests/VirtualGuy/Jump.png"
        self.image = pygame.image.load(self.genFilepath)
        self.imageRight = pygame.transform.scale(self.image, (self.w, self.h))
        self.imageLeft = pygame.transform.flip(self.imageRight, True, False)
        self.lastImage = self.imageRight
                        
    def movementPress(self, direction, pressed):     
        if direction == "right":
            self.rightPress = pressed
            self.lastPress = direction
        elif direction == "left":
            self.leftPress = pressed
            self.lastPress = direction
        elif direction == "space" and pressed:
            self.jump()
                               
    def jump(self):
        if self.grounded:
            self.grounded = False
            self.yv -= self.jumpVel
            
    def update(self):
        
        if self.rightPress and not self.leftPress:
            self.xv = self.maxXVel
        elif not self.rightPress and self.leftPress:
            self.xv = -self.maxXVel
        elif self.rightPress and self.leftPress:
            if self.lastPress == "right":
                self.xv = self.maxXVel
            else:
                self.xv = -self.maxXVel
        else:
            self.xv = 0            
        
        if not self.grounded:
            self.yv += self.g
            self.y += self.yv
        if not self.walled:    
            self.x += self.xv
                  
    def draw(self):
        if self.xv > 0:
            screen.blit(self.imageRight, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.imageRight
        elif self.xv < 0:
            screen.blit(self.imageLeft, pygame.Rect(self.x, self.y, self.w, self.h ))
            self.lastImage = self.imageLeft
        elif self.xv == 0:
            screen.blit(self.lastImage, pygame.Rect(self.x, self.y, self.w, self.h ))
            
