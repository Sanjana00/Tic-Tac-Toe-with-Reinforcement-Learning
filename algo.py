import sys

ROW1 = [0, 1, 2]
ROW2 = [3, 4, 5]
ROW3 = [6, 7, 8]

COL1 = [0, 3, 6]
COL2 = [1, 4, 7]
COL3 = [2, 5, 8]

LDIAG = [0, 4, 8]
RDIAG = [2, 4, 6]

CHECK = [ROW1, ROW2, ROW3, COL1, COL2, COL3, LDIAG, RDIAG]

def check_win(board):
    for line in CHECK:
        if board[line[0]] is None:
            continue
        if all(board[play] == board[line[0]] for play in line[1:]):
            return board[line[0]]
    return None

def check_draw(board):
    return all(play is not None for play in board)
