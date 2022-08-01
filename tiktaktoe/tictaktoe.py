import pygame

#hippyclipper

screenScale = 8
width = int(100 * screenScale)
height = width

UP = -1
DOWN = 1

RED = (231, 29, 54)
BLUE = (46, 196, 182)
BLACK = (1,22,39)
WHITE = (253, 255, 252)

LEFT_MOUSE = 1
RIGHT_MOUSE = 3
done = False

pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont('arial', 75)
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

class Board:
    
    def __init__(self,w,h):
        
        self.inGame = False
        self.text = "Start"
        self.startW = 100
        self.startH = 50
        self.textX = width//2-self.startW//2
        self.textY = height//2-self.startH//2
        self.textObj = font.render(self.text,True,RED)
       
        self.x = w//3
        self.y = h//3
        self.w = w
        self.h = h
        self.smallSide = 10
        
        self.rec1 = pygame.Rect(0,self.y, self.w, self.smallSide)
        self.rec2 = pygame.Rect(0,self.y*2, self.w, self.smallSide)       
        self.rec3 = pygame.Rect(self.x, 0, self.smallSide, self.h)
        self.rec4 = pygame.Rect(self.x*2, 0, self.smallSide, self.h)
        
    def draw(self):
        
        if not self.inGame:           
            screen.blit(self.textObj, self.textObj.get_rect(center = screen.get_rect().center))
        else:
            pygame.draw.rect(screen, RED, self.rec1)
            pygame.draw.rect(screen, RED, self.rec2)
            pygame.draw.rect(screen, RED, self.rec3)
            pygame.draw.rect(screen, RED, self.rec4)


class Piece:
    
    def __init__(self, x, y):
        
        self.x = x * width//3 + (width//3//2)
        self.y = y * height//3 + (height//3//2)
        self.r = 20
        
    def draw(self):
        
        pygame.draw.circle(screen, RED, (self.x, self.y), self.r)
        
        
class Cross(Piece):
    
    def __init__(self,x,y):
        
        super().__init__(x, y)
        
        offsetX = 50
        offsetY = 50
        
        self.xTop = (x*width//3) + offsetX
        self.yTop = (y*height//3) + offsetY
        self.xBot = x*width//3 + width//3 - offsetX
        self.yBot = y*height//3 + height//3 - offsetY
        
        self.xTop1 = (x*width//3) + width//3 - offsetX
        self.yTop1 = (y*height//3) + offsetY
        self.xBot1 = x*width//3 + offsetX
        self.yBot1 = y*height//3 + height//3 - offsetY
        
        self.thickness = 20
        
    def draw(self):
        
        pygame.draw.line(screen, BLUE, (self.xTop, self.yTop), (self.xBot, self.yBot), self.thickness)
        pygame.draw.line(screen, BLUE, (self.xTop1, self.yTop1), (self.xBot1, self.yBot1), self.thickness)
        
class Pieces:
    
    def __init__(self):
        
        self.pieces = []
        self.board = {}
        self.direct = ""
        self.end = (-1,-1)
        self.won = False
        
    def clear(self):
        
        self.pieces = []
        self.board = {}
        self.direct = ""
        self.end = (-1,-1)
        
    def checkEndGame(self, direction):
        
        ended = False
        player = None
        
        for x in range(3):
            
            ended = True
            player = None
            key = (0,0)
            
            for y in range(3):
                
                if direction == "down":
                    key = (x,y)
                elif direction == "right":
                    key = (y,x)                    
                elif direction == "diagLeft":
                    key = (y,y)                    
                elif direction == "diagRight":
                    key = (y,2-y)
                                      
                if not key in self.board:
                    ended = False
                    break
                elif y == 0:
                    player = self.board[key]
                elif not player == self.board[key]:
                    ended = False
                    break
                
            if not ended and "diag" in direction:
                return False
            
            if ended:
                self.direct = direction
                self.end = (key[0], key[1])
                self.won = True
                return ended
            
        return False
        
    def addNew(self,x,y, cirlceTurn):
        
        x = x//(width//3)
        y = y//(height//3)
        
        if (x,y) in self.board:
            return False
        
        self.board[(x,y)] = circleTurn
        
        if circleTurn:
            self.pieces.append(Piece(x,y))
        else:
            self.pieces.append(Cross(x,y))
            
        self.checkEndGame("right")
        self.checkEndGame("down")
        self.checkEndGame("diagLeft")
        self.checkEndGame("diagRight")
            
        return True
    
    def draw(self):

        first = None
        last = None
        
        for x in self.pieces:
            x.draw()
            
        if self.direct != "":
            
            if self.direct == "right":
                first = (0, self.end[1]*height//3+height//6)
                last = (width, self.end[1]*height//3+height//6)
            elif self.direct == "down":
                first = (self.end[0]*width//3+width//6, 0)
                last = (self.end[0]*width//3+width//6, height)
            elif self.direct == "diagLeft":
                first = (0,0)
                last = (width, height)
            else:
                first = (width, 0)
                last = (0, height)
                
            pygame.draw.line(screen, WHITE, first, last, 20)
            
        
board = Board(width, height)
pieces = Pieces()

circleTurn = True
nextClick = False

while not done:
    
    pressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            pass
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==  RIGHT_MOUSE:           
            x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE:
            x, y = pygame.mouse.get_pos()
            if board.inGame:
                added = pieces.addNew(x,y, circleTurn)
                if added:
                    circleTurn = not circleTurn
            elif board.textObj.get_rect(center = screen.get_rect().center).collidepoint((x,y)):
                board.inGame = True
            if nextClick:
                nextClick = False
                board = Board(width, height)
                pieces = Pieces()
            if pieces.won or len(pieces.board) == 9:
                nextClick = True

    board.draw()   
    pieces.draw()
    pygame.display.flip()
    clock.tick(60)
    screen.fill(BLACK)


pygame.display.quit()
pygame.quit()