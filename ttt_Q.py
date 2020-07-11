import pickle
import random
import numpy as np
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

CROSS = 1
NOUGHT = -1
EMPTY = 0

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

    def __init__(self, XO, p1, p2):
        self.XO = XO #current player
        self.p1 = p1
        self.p2 = p2
        self.winner = None
        self.draw = False
        self.board = [EMPTY] * 9
        self.boardHash = None

    def getHash(self):
        self.boardHash = str(self.board)
        
        print(self.boardHash)
        return self.boardHash

    def game_initiating_window(self): 
    
        screen.blit(initiating_window, (0, 0)) 
    
        pg.display.update() 
        time.sleep(3)                    
        screen.fill(white) 

        pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
        pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

        pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
        pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

    def check_win(self):
        for line in CHECK:
            if self.board[line[0]] is EMPTY:
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                pg.draw.line(*LINEARGS[line])
                self.winner = 'X' if self.board[line[0]] == 1 else 'O'

    def check_draw(self):
        self.draw = all(play is not EMPTY for play in self.board)

    def game_status(self): 
        curr = {1: 'X', -1: 'O'}
        if self.winner is None: 
            message = curr[self.XO] + "'s Turn"
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
        if pos is not None and self.board[pos] is EMPTY: 
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
        return [idx for idx, item in enumerate(self.board) if item is EMPTY]

    def give_reward(self):
        result = self.winner
        # backpropagate reward
        if result == CROSS:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == NOUGHT:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)

    def reset(self, XO, winner, draw, board, p1, p2):
        
        self.XO = XO #current player
        self.p1 = p1
        self.p2 = p2
        self.winner = winner
        self.draw = draw
        self.board = board
        self.boardHash = None

class Player:
    def __init__(self, name, exp_rate=0.3):
        self.name = name
        self.states = []  # record all positions taken
        self.lr = 0.2
        self.exp_rate = exp_rate
        self.decay_gamma = 0.9
        self.states_value = {}  # state -> value

    def getHash(self, board):
        boardHash = str(board)
        return boardHash

    def chooseAction(self, positions, current_board, symbol):
        if np.random.uniform(0, 1) <= self.exp_rate:
            # take random action
            #idx = np.random.choice(len(positions))
            #action = positions[idx]
            action = random.sample(positions, 1)[0]
        else:
            value_max = -999
            for p in positions:
                next_board = current_board.copy()
                next_board[p] = symbol
                next_boardHash = self.getHash(next_board)
                value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
                
                if value >= value_max:
                    value_max = value
                    action = p
                    
        return action

    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()


class HumanPlayer:
    def __init__(self, name):
        self.name = name

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass


#driver code

p1 = Player("computer", exp_rate = 0)
p1.loadPolicy("policy_p1")
p2 = HumanPlayer("human")

game = TicTacToe(CROSS, p1, p2)

game.game_initiating_window() 
game.game_status()

if game.XO == CROSS:
    positions = game.available()
    p1_action = p1.chooseAction(positions, game.board, game.XO)
    game.drawXO(p1_action)
    game.check_win()
    game.check_draw()
    game.game_status()

while(True): 
    for event in pg.event.get(): 
        #first player agent
        if event.type == QUIT: 
            pg.quit() 
            sys.exit() 
        
        elif event.type is MOUSEBUTTONDOWN: 
            game.user_click() 

            if game.XO == CROSS and not game.winner and not game.draw:
                positions = game.available()
                p1_action = p1.chooseAction(positions, game.board, game.XO)
                game.drawXO(p1_action)
                game.check_win()
                game.check_draw()
                game.game_status()

            if game.winner or game.draw:
                time.sleep(2)
                game.reset(CROSS, None, False, [EMPTY] * 9, p1, p2)
                pg.quit() 
                sys.exit() 
                break
    
    pg.display.update() 
    CLOCK.tick(fps) 
