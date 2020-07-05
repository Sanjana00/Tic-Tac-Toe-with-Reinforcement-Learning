import random
import pygame as pg 
import sys 
import time 
from pygame.locals import *

#   INITIALIZING DIMENSIONS OF THE GAME SCREEN

width, height = 400, 400

#   LIST CONTAINING COORDINATES OF THE CENTRE OF EACH SQUARE ON THE GRID
POSITIONS = list(zip([30, width / 3 + 30, width / 3 * 2 + 30] * 3, [30] * 3 + [height / 3 + 30] * 3 + [height / 3 * 2 + 30] * 3))

#   LIST CONTAINING THE COORDINATES OF THE EXTREMITIES (BOTTOM RIGHT CORNER) OF EACH SQUARE ON THE GRID
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
red = (255, 0, 0)
line_color = (0, 0, 0) 

CROSS = 'x'
NOUGHT = 'o'

pg.init() 

fps = 30

CLOCK = pg.time.Clock() 

screen = pg.display.set_mode((width, height + 100), 0, 32) 

pg.display.set_caption("Tic Tac Toe") 

#   DICTIONARY STORING LINES IN THE GRID AS KEYS AND PARAMETERS REQUIRED TO DRAW THE RED LINE THROUGH THEM ON WINNING
LINEWIDTH = 4
LINEARGS = {
    ROW1 : (screen, red, (20, height / 6), (width - 20, height / 6),LINEWIDTH),
    ROW2 : (screen, red, (20, height / 2), (width - 20, height / 2), LINEWIDTH),
    ROW3 : (screen, red, (20, height / 6 * 5), (width - 20, height / 6 * 5), LINEWIDTH),
    COL1 : (screen, red, (width / 6, 20), (width / 6, height - 20), LINEWIDTH),
    COL2 : (screen, red, (width / 2, 20), (width / 2, height - 20), LINEWIDTH),
    COL3 : (screen, red, (width / 6 * 5, 20), (width / 6 * 5, height - 20), LINEWIDTH),
    LDIAG: (screen, red, (50, 50), (350, 350), LINEWIDTH),
    RDIAG: (screen, red, (350, 50), (50, 350), LINEWIDTH)
    }

initiating_window = pg.image.load("bg1.png") 
x_img = pg.image.load("cross.jpg") 
y_img = pg.image.load("nought.png") 

initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

ICON = {CROSS : x_img, NOUGHT : o_img}

def game_initiating_window(): 
    ''' This function initialises the game window with the background image for 3 seconds before showing an empty grid for a new game '''
    screen.blit(initiating_window, (0, 0)) 
    
    pg.display.update() 
    time.sleep(3)                    
    screen.fill(white) 

    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

def check_win(board):
    ''' This functions checks if a winner is determined at the given state of the game '''
    for line in CHECK:
        if board[line[0]] is None:
            continue
        if all(board[play] == board[line[0]] for play in line[1:]):
            pg.draw.line(*LINEARGS[line])
            return board[line[0]]
    return None

def check_draw(board):
    ''' This functions checks if there are no available valid moves for any player (all squares occupied). This is the draw condition if there is no winner '''
    return all(play is not None for play in board)

def game_status(draw, winner, XO): 
    ''' This function prints the status of the game currently by deciding and displaying the message at the bottom of the grid on the game screen '''
    if winner is None: 
        message = XO.upper() + "'s Turn"
    else: 
        message = winner.upper() + " won !"
    if draw and winner is None: 
        message = "Game Draw !"

    font = pg.font.Font(None, 30) 
    
    text = font.render(message, 1, (255, 255, 255)) 

    screen.fill((0, 0, 0), (0, 400, 500, 100)) 
    text_rect = text.get_rect(center =(width / 2, 500-50)) 
    screen.blit(text, text_rect) 
    pg.display.update() 
    
    
def drawXO(pos, board, XO): 
    ''' This function assigns the value at a particular position on the board and displays the appropriate icon at the required position on the game screen '''
    posx, posy = POSITIONS[pos]
    board[pos] = XO 
    
    screen.blit(ICON[XO], (posx, posy))
    pg.display.update() 
    return board, flip(XO)

def get_square(): 
    ''' This function returns the index of the board depending on where the user has clicked on the game screen '''
    x, y = pg.mouse.get_pos() 
    for idx, limit in enumerate(LIMITS):
        xlim, ylim = limit
        if x < xlim and y < ylim:
            return idx
    return None

def user_click(board, XO, winner, draw):
    ''' This function updates the board and game status on user click on the game screen '''
    pos = get_square()
    if pos is not None and board[pos] is None: 
        board, XO = drawXO(pos, board, XO) 
        winner = check_win(board)
        draw = check_draw(board)
        game_status(draw, winner, XO)
    return board, XO, winner, draw
        
def flip(XO):
    ''' This function allows the switching of move control between the two players '''
    return CROSS if XO == NOUGHT else NOUGHT

def available(board):
    ''' This function returns a list of valid moves on the board '''
    return [idx for idx, item in enumerate(board) if item is None]

def rand_sel(board, XO, winner, draw):
    ''' This function allows the computer to make a random move '''
    pos = random.sample(available(board), 1)[0]
    board, XO = drawXO(pos, board, XO)
    winner = check_win(board)
    draw = check_win(board)
    game_status(draw, winner, XO)
    return board, XO, winner, draw


#==================================================================================
#   DRIVER CODE
#==================================================================================

XO = CROSS

winner = None

draw = False

board = [None] * 9

game_initiating_window() 
game_status(draw, winner, XO)

while True: 
    for event in pg.event.get(): 
        if event.type == QUIT: 
            pg.quit() 
            sys.exit() 
        elif event.type is MOUSEBUTTONDOWN: 
            board, XO, winner, draw = user_click(board, XO, winner, draw) 
            if XO == NOUGHT and not winner and not draw:
                time.sleep(0.5)
                board, XO, winner, draw = rand_sel(board, XO, winner, draw)
            if winner or draw:
                time.sleep(2)
                XO, winner, draw, board = CROSS, None, False, [None] * 9 
                game_initiating_window()
                game_status(draw, winner, XO)
    pg.display.update() 
    CLOCK.tick(fps) 

