from gameObject import GameObject
from constants import *
import math


class CollisionHandler(GameObject):
    
    def __init__(self):
        super().__init__(0,0)
     
    def hasCollidedPoint(self,square1, square2):
        
        rect1 = pygame.Rect(square1.x-(square1.w//4), square1.y-(square1.h//4), square1.w+(square1.w//2), square1.h+(square1.h//2))
        pointSquare2 = (square2.x+(square2.w//2), square2.y+(square2.h//2))

        return rect1.collidepoint(pointSquare2)        
        
    def hasCollided(self,square1, square2):
        
        rect1 = pygame.Rect(square1.x, square1.y, square1.w, square1.h)
        rect2 = pygame.Rect(square2.x, square2.y, square2.w, square2.h)
        
        return rect1.colliderect(rect2)
        
        
    def checkPlayerX(self, player, tile):
        walled = False
        playerRect = pygame.Rect(player.x, player.y, player.w, player.h)
        tileRect = pygame.Rect(tile.x, tile.y, tile.w, tile.h)
        movedPlayer = pygame.Rect(player.x, player.y, player.w, player.h)
        movedPlayer.x += player.xv
        movedCollides = movedPlayer.colliderect(tileRect)
        playerCollides = playerRect.colliderect(tileRect)
        
        if movedCollides and not playerCollides and player.xv > 0:
            player.x = tile.x - player.w
            player.xy = 0
            walled = True
            
        if movedCollides and not playerCollides and player.xv < 0:
            player.x = tile.x + tile.w
            player.xv = 0
            walled = True
            
        playerRect.x += 1
        
        if player.xv == 0 and playerRect.colliderect(tileRect):
            walled = True
            
        playerRect.x -= 2
        
        if player.xv == 0 and playerRect.colliderect(tileRect):
            walled = True
            
        playerRect.x += 1
        
        if playerRect.colliderect(tileRect):
            collidesTileLeft = abs((player.x+player.w) - tile.x) < abs(player.x - (tile.x + tile.w))
            if collidesTileLeft:
                player.x = tile.x - player.w
                player.xy = 0
                walled = True 
            else:
                player.x = tile.x + tile.w
                player.xv = 0
                walled = True              
                            
        return walled
        
        
    def checkPlayerY(self, player, tile):
        grounded = False
        playerRect = pygame.Rect(player.x, player.y, player.w, player.h)
        tileRect = pygame.Rect(tile.x, tile.y, tile.w, tile.h)
        movedPlayer = pygame.Rect(player.x, player.y, player.w, player.h)
        movedPlayer.y += player.yv
        movedCollides = movedPlayer.colliderect(tileRect)
        playerCollides = playerRect.colliderect(tileRect)
        
        if movedCollides and not playerCollides and player.yv > 0:
            player.y = tile.y - player.h
            player.yv = 0
            grounded = True
            
        if movedCollides and not playerCollides and player.yv < 0:
            player.y = tile.y + tile.h
            player.yv = 0
                    
        playerRect.y += 1
        
        if player.yv == 0 and playerRect.colliderect(tileRect):
            grounded = True
            
        return grounded
            
    def playerAndMap(self, player, level):
        grounded = False
        walled = False
        for row in level.level:
            for tile in row:
                if tile.name == "end":

                    if self.hasCollided(player,tile):
                        player.ended = True
                    else:
                        player.ended = False

                        
                if not tile.canCollide:
                    continue

                walled = walled or self.checkPlayerX(player, tile)
                grounded = grounded or self.checkPlayerY(player, tile)
                
        player.grounded = grounded
        player.walled = walled
        
    def playerAndItems(self, player, items):
        for item in items.items:
            if self.hasCollidedPoint(player,item):
                item.deleteMe = True

        
        