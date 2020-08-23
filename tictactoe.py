import random
import pygame as pg 
import pygame_menu
import sys 
import os
import csv
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
black = (0, 0, 0)

line_color = black 

CROSS = 'X'
NOUGHT = 'O'
EMPTY = '-'

# INITIALIZNG PYGAME
pg.init() 

fps = 30

CLOCK = pg.time.Clock() 

screen = pg.display.set_mode((width, height + 100), 0, 32) 

pg.display.set_caption("Tic Tac Toe") 

# DICTIONARY STORING LINES IN THE GRID AS KEYS AND PARAMETERS REQUIRED TO DRAW THE RED LINE THROUGH THEM ON WINNING

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
x_img = pg.image.load("cross.png") 
y_img = pg.image.load("nought.png") 

initiating_window = pg.transform.scale(initiating_window, (width, height + 100)) 
x_img = pg.transform.scale(x_img, (80, 80)) 
o_img = pg.transform.scale(y_img, (80, 80)) 

ICON = {CROSS : x_img, NOUGHT : o_img}

filename = 'state_values.csv'

class TicTacToe():

    def __init__(self):
        self.player = CROSS
        self.winner = None
        self.draw = False
        self.board = [EMPTY] * 9

    def game_initiating_window(self): 
        ''' This function initialises the game window with the background image for 1.5 seconds
        before showing an empty grid for a new game '''
  
        screen.blit(initiating_window, (0, 0)) 
    
        pg.display.update() 
        time.sleep(1.5)                    
        screen.fill(white) 

        pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7) 
        pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7) 

        pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7) 
        pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7) 

    def check_win(self):
        ''' This functions checks if a winner is determined at the given state of the game '''

        for line in CHECK:
            if self.board[line[0]] == EMPTY:
                continue
            if all(self.board[play] == self.board[line[0]] for play in line[1:]):
                pg.draw.line(*LINEARGS[line])
                self.winner = self.board[line[0]]

    def check_draw(self):
        ''' This functions checks if there are no available valid moves for any player (all squares occupied). 
        This is the draw condition if there is no winner '''

        self.draw = all(play != EMPTY for play in self.board)

    def playable(self):
        self.check_win()
        self.check_draw()
        return not self.draw and not self.winner

    def game_status(self): 
        ''' This function prints the status of the game currently by deciding 
        and displaying the message at the bottom of the grid on the game screen '''
 
        if self.winner is None: 
            message = self.player + "'s Turn"
        else: 
            message = self.winner + " won !"
        if self.draw and self.winner is None: 
            message = "Game Draw !"

        font = pg.font.Font(pg.font.get_default_font(), 30) 
    
        text = font.render(message, 1, (255, 255, 255)) 

        screen.fill((0, 0, 0), (0, 400, 500, 100)) 
        text_rect = text.get_rect(center =(width / 2, 500-50)) 
        screen.blit(text, text_rect) 
        pg.display.update() 
    
    
    def make_move(self, pos):
        ''' This function assigns the value at a particular position on the board and 
        displays the appropriate icon at the required position on the game screen '''

        posx, posy = POSITIONS[pos]
        self.board[pos] = self.player 
    
        screen.blit(ICON[self.player], (posx, posy))
        pg.display.update() 
        self.flip()
        self.check_win()
        self.check_draw()

    def get_square(self):
        ''' This function returns the index of the board 
        depending on where the user has clicked on the game screen '''
        
        x, y = pg.mouse.get_pos() 
        for idx, limit in enumerate(LIMITS):
            xlim, ylim = limit
            if x < xlim and y < ylim:
                return idx
        return None

    def user_click(self):
        ''' This function updates the board and game status on user click on the game screen '''

        pos = self.get_square()
        if pos is not None and self.board[pos] == EMPTY: 
            self.make_move(pos) 
        
    def flip(self):
        ''' This function allows the switching of move control between the two players '''

        if self.player == NOUGHT:
            self.player = CROSS
        else:
            self.player = NOUGHT

    def valid_moves(self):
        ''' This function returns a list of valid moves on the board '''

        return [idx for idx, item in enumerate(self.board) if item == EMPTY]


class Agent():
    def __init__(self, game_class, epsilon = 0.1, alpha = 0.5, value_player = CROSS):
        self.V = dict()
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha
        self.value_player = value_player

    def learn_game(self, num_episodes = 1000):
        for episode in range(num_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        game = self.NewGame()
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)

    def learn_select_move(self, game):
        allowed_state_values = self.__state_values(self.form_states(game, game.valid_moves()))
        if game.player == self.value_player:
            best_move = self.choose_state(allowed_state_values, True)
        else:
            best_move = self.choose_state(allowed_state_values, False)

        selected_move = best_move
        if random.random() < self.epsilon:
            selected_move = self.__random_V(allowed_state_values)

        return best_move, selected_move
    
    def __random_V(self, state_values):
        return random.choice(list(state_values.keys()))
    
    def learn_from_move(self, game, move):
        game.make_move(self.find_pos(game, move))
        r = self.__reward(game)
        td_target = r
        next_state_value = 0.0
        selected_next_move = None
        if game.playable():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)
        current_state_value = self.state_value(move)
        td_target = r + next_state_value
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        return selected_next_move


    def __reward(self, game):
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    def interactive_game(self, agent_player = NOUGHT):
        game = self.NewGame()
        game.game_initiating_window()
        game.game_status()
        while True:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif game.player == agent_player:
                    time.sleep(0.5)
                    move = self.play_select_move(game)
                    game.make_move(self.find_pos(game, move))
                    game.game_status()
                elif event.type is MOUSEBUTTONDOWN:
                    game.user_click()
                    game.game_status()
                if game.winner or game.draw:
                    time.sleep(2)
                    game = self.NewGame()
                    game.game_initiating_window()
                    game.game_status()
            pg.display.update()
            CLOCK.tick(fps)

    def find_pos(self, game, state):
        for idx, item in enumerate(state):
            if item != game.board[idx]:
                return idx
        return None
    
    def choose_state(self, state_values, is_agent_player):
        values = state_values.values()
        val = max(values) if is_agent_player else min(values)
        chosen_state = random.choice([state for state, v in state_values.items() if v == val])
        return chosen_state
    
    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)
    
    def __state_values(self, game_states):
        return dict((state, self.state_value(state)) for state in game_states)
    
    def form_states(self, game, positions):
        possible_states = []
        for pos in positions:
            new_state = game.board[:]
            new_state[pos] = game.player
            possible_states.append(''.join(new_state))
        return possible_states

    def play_select_move(self, game):
        allowed_state_values = self.__state_values(self.form_states(game, game.valid_moves()))
        if game.player == self.value_player:
            return self.choose_state(allowed_state_values, True)
        return self.choose_state(allowed_state_values, False)
    
    def demo_game(self):
        game = self.NewGame()
        while game.playable():
            move = self.play_select_move(game)
            game.make_move(self.find_pos(game, move))
        if game.winner:
            return game.winner
        return '-'

    def round_V(self):
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)
    
    def save_v_table(self):
        with open(filename, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            all_states = list(self.V.keys())
            all_states.sort()
            for state in all_states:
                writer.writerow([state, self.V[state]])

    def retrieve_v_table(self):
        if os.path.isfile(filename):
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row == ['State', 'Value']:
                        continue
                    self.V[row[0]] = float(row[1])

def demo_game_stats(agent):
    results = [agent.demo_game() for i in range(10000)]
    game_stats = {k: results.count(k) / 100 for k in [CROSS, NOUGHT, '-']}
    print('     percentage results: {}'.format(game_stats))

def play_CROSS():
    agent.interactive_game()

def play_NOUGHT():
    agent.interactive_game(agent_player = CROSS)

agent = Agent(TicTacToe, epsilon = 0.1, alpha = 1.0)

agent.retrieve_v_table()

train = input("Train the agent [Y/n]?: ")

if train.upper() == 'Y':
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

    agent.learn_game(20000)
    print('After 50000 learning games:')
    demo_game_stats(agent)

    agent.round_V()
    agent.save_v_table()

#mytheme = pygame_menu.themes.THEME_BLUE.copy()
#mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
#mytheme.font = pygame_menu.font.FONT_OPEN_SANS
#mytheme.cursor_selection_color((0, 0, 0))
#mytheme.title_font_color = black
#mytheme.title_shadow = False
mytheme = pygame_menu.themes.Theme(title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE, title_shadow = False, title_background_color=(4, 47, 126), title_font = pygame_menu.font.FONT_OPEN_SANS_ITALIC, background_color = (0, 60, 255, 100) )
menu = pygame_menu.Menu(height + 99, width - 1, 'Choose Icon',  theme = mytheme)

menu.add_button(CROSS, play_CROSS)
menu.add_button(NOUGHT, play_NOUGHT)
menu.mainloop(screen)

