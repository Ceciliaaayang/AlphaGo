import numpy as np
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER, \
                       PASS, is_black_white, coord_to_point, where1d, \
                       MAXSIZE, NULLPOINT

class TranspositionTable(object):
    
    def __init__(self, boardsize):
        self.table = dict()
        
        # Prepare one random number code[point][color] for each (point, color) combination
        self.state_code = dict()
        for point in range(boardsize):
            self.state_code[(point, EMPTY)] = np.random.randint(1,2147483647)
            self.state_code[(point, BLACK)] = np.random.randint(1,2147483647)
            self.state_code[(point, WHITE)] = np.random.randint(1,2147483647)
    
    # Used to print the whole table with print(tt)
    def __repr__(self):
        return self.table.__repr__()

    def store(self, code, score):
        self.table[code] = score

    # Python dictionary returns 'None' if key not found by get()
    def lookup(self, code):
        return self.table.get(code)

    # Zobrist Hash Codes
    def hash_code(self, state):
        hashcode = state.current_player
        for point in range(state.board.size):
            if state.board[point] != BORDER:
                hashcode = hashcode ^ self.state_code[(point, state.board[point])]
        return hashcode
