import pygame
import random
import math
from constants import * 
from gameObject import GameObject
from mapObj import Map
from ItemObj import Items
from CollisionHandlerObj import CollisionHandler
from PlayerObj import Player

#==========================================================================================================================
#TODO
#add player animation (idle, running, jumping, falling) 
#add enenmys (hardest, least needed)
#==========================================================================================================================
#COPYPASTA
# self.image = pygame.image.load(self.filepath)
# self.image = pygame.transform.scale(self.image, (self.w, self.h))
# screen.blit(self.image, pygame.Rect(self.x, self.y, self.w, self.h ))
# self.image = pygame.image.load(self.filepath)
# self.imageLeft = pygame.transform.flip(self.imageRight, vertical=True, horizontial=False)
#==========================================================================================================================
class Game:
    
    def __init__(self):
        self.level = Map()
        self.player = Player(self.level)
        self.items = Items(self.level)
        self.collisionHandler = CollisionHandler()
        
    def buttonEvent(self, direction, pressed):
        self.player.movementPress(direction, pressed)
        
    def handleCollisions(self):
        self.collisionHandler.playerAndMap(self.player, self.level)
        
    def update(self):
        self.handleCollisions()
        self.level.update()
        self.items.update()
        self.player.update()
    
    def draw(self):
        self.level.draw()
        self.items.draw()
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
            game.buttonEvent("left", False)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", True)
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            game.buttonEvent("right", False)
            
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
        
        
        
        
