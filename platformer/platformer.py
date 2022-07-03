import pygame
import random
import math
from constants import * 
from gameObject import GameObject
from mapObj import Map, Player

#==========================================================================================================================

class CollisionHandler(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
        
    def checkPlayerY(self, player, tile):
        
        playerRect = pygame.Rect(player.x, player.y, player.w, player.h)
        tileRect = pygame.Rect(tile.x, tile.y, tile.w, tile.h)
        movedPlayer = pygame.Rect(player.x, player.y, player.w, player.h)
        movedPlayer.y += player.yv
        movedCollides = movedPlayer.colliderect(tileRect)
        playerCollides = playerRect.colliderect(tileRect)
        if movedCollides and not playerCollides and player.yv > 0:
            player.y = tile.y - player.h
            player.yv = 0
            player.grounded = True
        if movedCollides and not playerCollides and player.yv < 0:
            player.y = tile.y + tile.h
            player.yv = 0

            
        
        
        
    
    def playerAndMap(self, player, level):
        for row in level.level:
            for tile in row:
                if not tile.canCollide:
                    continue
                self.checkPlayerY(player, tile)

            

#==========================================================================================================================
        
class Game:
    
    def __init__(self):
        self.level = Map()
        self.player = Player(self.level)
        self.collisionHandler = CollisionHandler()
        
    def buttonEvent(self, direction, pressed):
        print(direction, "pressed =", pressed)
        if direction == "space" and pressed:
            self.player.jump()
        
    def handleCollisions(self):
        self.collisionHandler.playerAndMap(self.player, self.level)
        
    def update(self):
        self.handleCollisions()
        self.level.update()
        self.player.update()
    
    def draw(self):
        self.level.draw()
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
                   
    game.draw()
    game.update()
            
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BACKGROUND)
    
#==========================================================================================================================
pygame.display.quit()
pygame.quit()    
        
        
        
        
