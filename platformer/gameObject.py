from constants import * 
import pygame

class GameObject:
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.xv = 0 
        self.yv = 0
        self.r = 10
        self.color = WHITE
        self.g = 10
        self.h = self.r
        self.w = self.r
        
    def update(self):
        self.x += self.xv
        self.y += self.yv
        
    def calcVector(self, rad, scale):
        x = math.cos(rad) * scale
        y = math.sin(rad) * scale
        return (x,y)
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)