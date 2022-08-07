import pygame
import os, sys
from pygame.locals import *
import math

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try: 
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image, image.get_rect()

class Square():
    def __init__(self,width,height,xpos,ypos):
        self.height = height
        self.width = width
        self.xpos = xpos
        self.ypos = ypos
        self.empty = True
        self.tellIfHighlight = False
        self.inside = 0

    def highlight(self, screen):
        if self.empty == True:
            x, y = pygame.mouse.get_pos()
            highlight = pygame.Surface((self.width-10, self.height-10))
            highlight.fill((255,0,0))
            highlight.set_alpha(82)
            highlight.convert_alpha()
            if (x>self.xpos+5 and x<self.xpos+self.width-5):
                if(y>self.ypos+5 and y<self.ypos+self.height-5):
                    screen.blit(highlight, ((self.xpos+5,self.ypos+5)))
                    self.tellIfHighlight = True
                else:
                    self.tellIfHighlight = False
            else:
                self.tellIfHighlight = False
        if self.empty == False:
            self.tellIfHighlight = False

    def draw(self,background):
        Square = pygame.Surface((self.width, self.height))
        Square.fill((0,0,0))
        Square.convert()
        inside = pygame.Surface((self.width-10, self.height-10))
        inside.fill((255,255,255))
        inside.convert()
        background.blit(Square, (self.xpos,self.ypos))
        background.blit(inside, (self.xpos+5,self.ypos+5))

    def drawCirc(self, background):
        pygame.draw.circle(background, (0,0,255), (self.xpos+(self.width/2),self.ypos+(self.height/2)),50)
        pygame.draw.circle(background, (255,255,255), (self.xpos+(self.width/2),self.ypos+(self.height/2)), 42)

    def drawX(self,background):
        z=10
        for x in range(z):
            pygame.draw.aaline(background, (255,0,0), (self.xpos+20+x-(z/2),self.ypos+20),(self.xpos+self.width-20+x-(z/2),self.ypos+self.height-20))
            pygame.draw.aaline(background, (255,0,0), (self.xpos+20+x-(z/2),self.ypos-20+self.height),(self.xpos+self.width-20+x-(z/2),self.ypos+20))
    
    def isfilled(self,answer, inside):
        self.inside = inside

        if answer == 1:
            self.empty = False
        else:
            self.empty = True
    
    def ishighlighted(self):
        return self.tellIfHighlight
    
    def getInside(self):
        return self.inside
    
    def getEmpty(self):
        return self.empty
    

class Grid():
    def __init__(self, xpos, ypos, size):
        self.xpos = xpos
        self.ypos = ypos
        self.size = size 
        self.squares = []
        self.turn = 0
        self.winon = 1
        self.alreadyWon = False
        self.xWins = 0
        self.oWins = 0
        self.array = [0]*9
        self.finish = False
        self.gameLength = 0
        self.winner = 0
        self.once = 0
        self.updated = 0

        y=0
        for i in ['A','B','C']:
            for x in range(3):
                name = "square"+str(i)+str(x)
                name = Square(self.size, self.size,self.xpos+(x*(self.size-5)),self.ypos+(y*(self.size-5)))
                self.squares.append(name)
            y+=1
    def drawGrid(self,background):
        for square in self.squares:
           square.draw(background)
        if pygame.font:
            font = pygame.font.Font(None, 50)
            text = font.render("X wins:", 1, (255, 10, 10))
            background.blit(text, (5,560))
        if pygame.font:
            font = pygame.font.Font(None, 50)
            text = font.render("O wins:", 1, (10, 10, 255))
            background.blit(text, (300,560))    


    def highlightGrid(self,screen):
        for square in self.squares:
            square.highlight(screen)
    
    def update(self,background):
        if self.turn == 0:
            for square in self.squares:
                if (square.ishighlighted()==True):
                    square.drawX(background)
                    square.isfilled(1,1)
                    self.turn = 2
        if self.turn == 1:
            for square in self.squares:
                if (square.ishighlighted()==True):
                    square.drawCirc(background)
                    square.isfilled(1,2)
                    self.turn = 3
        if self.turn == 2:
            self.turn = 1
            self.updated+=1
        if self.turn == 3:
            self.turn = 0
            self.updated+=1
        
    def clear(self, background):
        background.fill((250,250,250))
        self.drawGrid(background)
        for square in self.squares:
            square.isfilled(0,0)
            self.turn = 0
        self.winon = 1
        self.alreadyWon = False
        self.finish = False
        self.gameLength = 0
        self.winner = 0
        self.once = 0
        self.updated = 0

    def winScreen(self,background):
        self.winner = self.win()
        allHighlight = True
        if self.winner == 1:
            winnerText = "X"
            self.xWins+=1
        if self.winner == 2:
            winnerText = "O"
            self.oWins +=1
        if self.winner != None:
            if pygame.font:
                font = pygame.font.Font(None, 50)
                text = font.render("Player "+ winnerText + " Wins!", 1, (10, 10, 10))
                textpos = text.get_rect(centerx=background.get_width()/2)
                background.blit(text, textpos)
            self.alreadyWon = True
            for square in self.squares:
                square.isfilled(1,0)
            self.finish = True
        for square in self.squares:
            if square.getEmpty() == True:
                allHighlight = False
        if allHighlight == True and self.alreadyWon == False:
            if pygame.font:
                font = pygame.font.Font(None, 50)
                text = font.render("Its a draw!", 1, (10, 10, 10))
                textpos = text.get_rect(centerx=background.get_width()/2)
                background.blit(text, textpos)
            for square in self.squares:
                square.isfilled(1,0)
            self.finish = True
    
    def getWins(self):
        return self.xWins, self.oWins
    def win(self):
        index2 = 0
        for index in range(3):
            if self.winon == 1:
                if self.squares[index].getInside() != 0:
                    #Collumns
                    if self.squares[index].getInside() == self.squares[index+3].getInside() == self.squares[index+6].getInside():
                        self.winon = 0
                        return self.squares[index].getInside()
                    #Diagonals
                    elif index == 0:
                        if self.squares[index].getInside() == self.squares[index+4].getInside() == self.squares[index+8].getInside():
                            self.winon = 0
                            return self.squares[index].getInside()
                    elif index ==2:
                        if self.squares[index].getInside() == self.squares[index+2].getInside() == self.squares[index+4].getInside():
                            self.winon = 0
                            return self.squares[index].getInside()
                #Rows
                if self.squares[index2].getInside() != 0:
                    if self.squares[index2].getInside() == self.squares[index2+1].getInside() == self.squares[index2+2].getInside():
                        self.winon = 0
                        return self.squares[index2].getInside()
                index2+=3
    def setArray(self):
        index = 0
        for square in self.squares:
            self.array[index] = float(square.getInside())
            index+=1
    def getArray(self):
        return self.array


def main():
    
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption('Tic Tac Toe')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    TicTac = Grid(105,125,125)
    TicTac.drawGrid(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
    allsprites = pygame.sprite.RenderPlain()
    clock = pygame.time.Clock()
    prevUpdate = 0
    while 1:
        clock.tick(60)
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        TicTac.highlightGrid(screen)
        TicTac.winScreen(background)

        Xwins,Owins = TicTac.getWins()
        if pygame.font:
            font = pygame.font.Font(None, 50)
            text = font.render(str(Xwins), 1, (10, 10, 10))
            screen.blit(text, (150,560))
        if pygame.font:
                font = pygame.font.Font(None, 50)
                text = font.render(str(Owins), 1, (10, 10, 10))
                screen.blit(text, (450,560))


        if TicTac.finish == True:
            if TicTac.once == 0:
                TicTac.once +=1

        prevUpdate = TicTac.updated

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                return()
            elif event.type == MOUSEBUTTONDOWN:
                TicTac.update(background)
                TicTac.setArray()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return()
            elif event.type == KEYUP:
                TicTac.clear(background)
if __name__ == "__main__":
    main()

    
