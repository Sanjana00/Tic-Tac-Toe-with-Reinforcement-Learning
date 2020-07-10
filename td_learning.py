import random
import pygame as pg 
import sys 
import csv
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

    def __init__(self):
        self.player = CROSS
        self.winner = None
        self.draw = False
        self.board = ['-'] * 9

    def game_initiating_window(self): 
    
        screen.blit(initiating_window, (0, 0)) 
    
        pg.display.update() 
        time.sleep(1.5)                    
        screen.fill(white) 

        pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
        pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

        pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
        pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

    def check_win(self):
        for line in CHECK:
            if self.board[line[0]] == '-':
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                pg.draw.line(*LINEARGS[line])
                self.winner = self.board[line[0]]

    def check_draw(self):
        self.draw = all(play != '-' for play in self.board)
        return self.draw

    def game_status(self): 
    
        if self.winner is None: 
            message = self.player + "'s Turn"
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
    
    
    def make_move(self, pos): 
        posx, posy = POSITIONS[pos]
        self.board[pos] = self.player 
    
        screen.blit(ICON[self.player], (posx, posy))
        pg.display.update() 
        self.flip()
        self.check_win()

    def get_square(self): 
        x, y = pg.mouse.get_pos() 
        for idx, limit in enumerate(LIMITS):
            xlim, ylim = limit
            if x < xlim and y < ylim:
                return idx
        return None

    def user_click(self):
        pos = self.get_square()
        if pos is not None and self.board[pos] == '-': 
            self.make_move(pos) 
            self.check_win()
            self.check_draw()
            self.game_status()
        
    def flip(self):
        if self.player == NOUGHT:
            self.player = CROSS
        else:
            self.player = NOUGHT

    def valid_moves(self):
        return [idx for idx, item in enumerate(self.board) if item == '-']

    def rand_sel(self):
        pos = random.choice(self.valid_moves())
        self.make_move(pos)
        self.check_win()
        self.check_draw()
        self.game_status()


class Agent():
    def __init__(self, game_class, epsilon = 0.1, alpha = 0.5, value_player = CROSS):
        self.V = dict()
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha
        self.value_player = value_player

    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)

    def find_pos(self, game, state):
        for idx, item in enumerate(state):
            if item != game.board[idx]:
                return idx
        return None

    def learn_game(self, num_episodes = 1000):
        for episode in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        game = self.NewGame()
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)

    def form_states(self, game, positions):
        possible_states = []
        for pos in positions:
            new_state = game.board[:]
            new_state[pos] = game.player
            possible_states.append(''.join(new_state))
        return possible_states

    def learn_from_move(self, game, move):
        game.make_move(self.find_pos(game, move))
        r = self.__reward(game)
        td_target = r
        next_state_value = 0.0
        selected_next_move = None
        if not game.check_draw():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)
        current_state_value = self.state_value(move)
        td_target = r + next_state_value
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        return selected_next_move

    def learn_select_move(self, game):
        allowed_state_values = self.__state_values(self.form_states(game, game.valid_moves()))
        if game.player == self.value_player:
            best_move = self.__argmax_V(allowed_state_values)
        else:
            best_move = self.__argmin_V(allowed_state_values)

        selected_move = best_move
        if random.random() < self.epsilon:
            selected_move = self.__random_V(allowed_state_values)

        return best_move, selected_move

    def play_select_move(self, game):
        allowed_state_values = self.__state_values(self.form_states(game, game.valid_moves()))
        if game.player == self.value_player:
            return self.__argmax_V(allowed_state_values)
        return self.__argmin_V(allowed_state_values)

    def demo_game(self):
        game = self.NewGame()
        while not game.check_draw():
            move = self.play_select_move(game)
            game.make_move(self.find_pos(game, move))
        if game.winner:
            return game.winner
        return '-'

    def interactive_game(self, agent_player = NOUGHT):
        game = self.NewGame()
        while not game.check_draw():
            if game.player == agent_player:
                move = self.play_select_move(game)
                game.make_move(self.find_pos(game, move))
            else:
                move = self.__request_human_move(game)
                game.make_move(move)

        if game.winner:
            return game.winner
        return '-'

    def round_V(self):
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)

    def save_v_table(self):
        with open('state_values.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            all_states = list(self.V.keys())
            all_states.sort()
            for state in all_states:
                writer.writerow([state, self.V[state]])

    def __state_values(self, game_states):
        return dict((state, self.state_value(state)) for state in game_states)

    def __argmax_V(self, state_values):
        values = state_values.values()
        max_V = max(values)
        chosen_state = random.choice([state for state, v in state_values.items() if v == max_V])
        return chosen_state

    def __argmin_V(self, state_values):
        values = state_values.values()
        min_V = min(values)
        chosen_state = random.choice([state for state, v in state_values.items() if v == min_V])
        return chosen_state

    def __random_V(self, state_values):
        return random.choice(list(state_values.keys()))

    def __reward(self, game):
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    #def __request_human_move(self, game)

def demo_game_stats(agent):
    results = [agent.demo_game() for i in range(10000)]
    game_stats = {k: results.count(k) / 100 for k in [CROSS, NOUGHT, '-']}
    print('     percentage results: {}'.format(game_stats))


agent = Agent(TicTacToe, epsilon = 0.1, alpha = 1.0)
print('Before learning:')
demo_game_stats(agent)

agent.learn_game(1000)
print('After 1000 learning games:')
demo_game_stats(agent)

agent.learn_game(4000)
print('After 5000 learning games:')
demo_game_stats(agent)

agent.learn_game(5000)
print('After 10000 learning games:')
demo_game_stats(agent)

agent.learn_game(10000)
print('After 20000 learning games:')
demo_game_stats(agent)

agent.learn_game(10000)
print('After 30000 learning games:')
demo_game_stats(agent)

'''
#driver code

game = TicTacToe()

game.game_initiating_window() 
game.game_status()

while(True): 
    for event in pg.event.get(): 
        if event.type == QUIT: 
            pg.quit() 
            sys.exit() 
        elif event.type is MOUSEBUTTONDOWN: 
            game.user_click() 
            if game.player == NOUGHT and not game.winner and not game.draw:
                time.sleep(0.5)
                game.rand_sel()
            if game.winner or game.draw:
                time.sleep(2)
                game = TicTacToe()
                game.game_initiating_window()
                game.game_status()
    pg.display.update() 
    CLOCK.tick(fps) 
'''
