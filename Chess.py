# Chess class for logic etc
# Author: Jack Liu
# 12/27/2019


class Chess:
    board_map = {}

    # Constructor
    def __init__(self):
        self.board = {}
        self.turn = 'w'
        self.castling = 'KQkq'
        self.en_passant = '-'
        self.half_clock = 0
        self.move_number = 0
        self.construct()

    # Helper method for constructor
    def construct(self):
        # Creating the board
        self.board['8'] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self.board['7'] = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
        self.board['6'] = ['', '', '', '', '', '', '', '']
        self.board['5'] = ['', '', '', '', '', '', '', '']
        self.board['4'] = ['', '', '', '', '', '', '', '']
        self.board['3'] = ['', '', '', '', '', '', '', '']
        self.board['2'] = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        self.board['1'] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        # Creating the board map
        self.board_map['a'] = 0
        self.board_map['b'] = 1
        self.board_map['c'] = 2
        self.board_map['d'] = 3
        self.board_map['e'] = 4
        self.board_map['f'] = 5
        self.board_map['g'] = 6
        self.board_map['h'] = 7

    # Returns a FEN string corresponding to the board
    def to_string(self):
        to_return = ''
        s_count = 0
        for key in self.board:
            for space in self.board[key]:
                if space is not '':
                    if s_count is not 0:
                        to_return += str(s_count)
                        s_count = 0
                    to_return += space
                else:
                    s_count += 1
            if s_count is not 0:
                to_return += str(s_count)
                s_count = 0
            to_return += '/'
        to_return = '{0} {1} {2} {3} {4} {5}'.format(to_return[0:-1], self.turn, self.castling, self.en_passant,
                                                     str(self.half_clock), str(self.move_number))
        return to_return
