import random
import pygame as pg 
import sys 
import time 
from pygame.locals import *

width, height = 400, 400

POSITIONS = list(zip([30, width / 3 + 30, width / 3 * 2 + 30] * 3, [30] * 3 + [height / 3 + 30] * 3 + [height / 3 * 2 + 30] * 3))

LIMITS = list(zip([width / 3, width / 3 * 2, width] * 3, [height / 3] * 3 + [height / 3 * 2] * 3 + [height] * 3))
                
ROW1 = (0, 1, 2)
ROW2 = (3, 4, 5)
ROW3 = (6, 7, 8)

COL1 = (0, 3, 6)
COL2 = (1, 4, 7)
COL3 = (2, 5, 8)

LDIAG = (0, 4, 8)
RDIAG = (2, 4, 6)
 
CHECK = [ROW1, ROW2, ROW3, COL1, COL2, COL3, LDIAG, RDIAG]
               
white = (255, 255, 255) 

line_color = (0, 0, 0) 

CROSS = 'X'
NOUGHT = 'O'

pg.init() 

fps = 30

CLOCK = pg.time.Clock() 

screen = pg.display.set_mode((width, height + 100), 0, 32) 

pg.display.set_caption("Tic Tac Toe") 

LINEARGS = {
    ROW1 : (screen, (250, 0, 0), (20, height / 6), (width - 20, height / 6), 4),
    ROW2 : (screen, (250, 0, 0), (20, height / 2), (width - 20, height / 2), 4),
    ROW3 : (screen, (250, 0, 0), (20, height / 6 * 5), (width - 20, height / 6 * 5), 4),
    COL1 : (screen, (250, 0, 0), (width / 6, 20), (width / 6, height - 20), 4),
    COL2 : (screen, (250, 0, 0), (width / 2, 20), (width / 2, height - 20), 4),
    COL3 : (screen, (250, 0, 0), (width / 6 * 5, 20), (width / 6 * 5, height - 20), 4),
    LDIAG: (screen, (250, 0, 0), (50, 50), (350, 350), 4),
    RDIAG: (screen, (250, 0, 0), (350, 50), (50, 350), 4)
    }

initiating_window = pg.image.load("bg1.png") 
x_img = pg.image.load("cross.jpg") 
y_img = pg.image.load("nought.png") 

initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

ICON = {CROSS : x_img, NOUGHT : o_img}

class TicTacToe():

    def __init__(self, XO, winner, draw, board):
        self.XO = XO
        self.winner = winner
        self.draw = draw
        self.board = board

    def drawtext(self, text, color, surface, x, y):
        font = pg.font.SysFont(None, 30)
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def button(self):
        click = False  
        screen.fill(white)
        self.drawtext("menu", (200, 200, 200), screen, 20, 20)
        mx, my = pg.mouse.get_pos()

        button1 = pg.Rect(50, 100, 200, 50)
        button2 = pg.Rect(50, 200, 200, 50)

        if button1.collidepoint((mx, my)):
            if click:
                #self.XO = NOUGHT
                self.game_initiating_window()

        if button1.collidepoint((mx, my)):
            if click:
                #self.XO = CROSS
                self.game_initiating_window()
        
        pg.draw.rect(screen, (255, 0, 0), button1)
        pg.draw.rect(screen, (255, 0, 0), button2)
        
        click = False
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pg.display.update()
        CLOCK.tick(fps)

    def game_initiating_window(self): 
    
        screen.blit(initiating_window, (0, 0)) 
    
        pg.display.update() 
        time.sleep(3)                    
        screen.fill(white) 

        time.sleep(2)
        pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
        pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

        pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
        pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

        
        game.game_status()


    def check_win(self):
        for line in CHECK:
            if self.board[line[0]] is None:
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                pg.draw.line(*LINEARGS[line])
                self.winner = self.board[line[0]]

    def check_draw(self):
        self.draw = all(play is not None for play in self.board)

    def game_status(self): 
    
        if self.winner is None: 
            message = self.XO + "'s Turn"
        else: 
            message = self.winner + " won !"
        if self.draw and self.winner is None: 
            message = "Game Draw !"

        font = pg.font.Font(None, 30) 
    
        text = font.render(message, 1, (255, 255, 255)) 

        screen.fill((0, 0, 0), (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(width / 2, 500-50)) 
        screen.blit(text, text_rect) 
        pg.display.update() 
    
    
    def drawXO(self, pos): 
        posx, posy = POSITIONS[pos]
        self.board[pos] = self.XO 
    
        screen.blit(ICON[self.XO], (posx, posy))
        pg.display.update() 
        self.flip()

    def get_square(self): 
        x, y = pg.mouse.get_pos() 
        for idx, limit in enumerate(LIMITS):
            xlim, ylim = limit
            if x < xlim and y < ylim:
                return idx
        return None

    def user_click(self):
        pos = self.get_square()
        if pos is not None and self.board[pos] is None: 
            self.drawXO(pos) 
            self.check_win()
            self.check_draw()
            self.game_status()
        
    def flip(self):
        if self.XO == NOUGHT:
            self.XO = CROSS
        else:
            self.XO = NOUGHT

    def available(self):
        return [idx for idx, item in enumerate(self.board) if item is None]

    def rand_sel(self):
        pos = random.sample(self.available(), 1)[0]
        self.drawXO(pos)
        self.check_win()
        self.check_draw()
        self.game_status()

#driver code

game = TicTacToe(CROSS, None, False, [None] * 9)

game.game_initiating_window() 
game.game_status()
while(True): 
    for event in pg.event.get(): 
        if event.type == QUIT: 
            pg.quit() 
            sys.exit() 
        elif event.type is MOUSEBUTTONDOWN: 
            game.user_click() 
            if game.XO == NOUGHT and not game.winner and not game.draw:
                time.sleep(0.5)
                game.rand_sel()
            if game.winner or game.draw:
                time.sleep(2)
                game = TicTacToe(CROSS, None, False, [None] * 9)
                game.game_initiating_window()
                game.game_status()
    pg.display.update() 
    CLOCK.tick(fps) 
