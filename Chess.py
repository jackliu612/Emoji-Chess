# Chess class for logic etc
# Author: Jack Liu
# 12/27/2019
import pyperclip


class Chess:
    board_map = {}

    # Constructor
    def __init__(self):
        self.board = []
        self.turn = 'w'
        self.castling = 'KQkq'
        self.en_passant = '-'
        self.half_clock = 0
        self.move_number = 1
        self.construct()

    # Helper method for constructor
    def construct(self):
        # Creating the board
        # self.board['8'] = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        # self.board['7'] = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
        # self.board['6'] = ['', '', '', '', '', '', '', '']
        # self.board['5'] = ['', '', '', '', '', '', '', '']
        # self.board['4'] = ['', '', '', '', '', '', '', '']
        # self.board['3'] = ['', '', '', '', '', '', '', '']
        # self.board['2'] = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        # self.board['1'] = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                      ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['', '', '', '', '', '', '', ''],
                      ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                      ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
        # Creating the board map
        self.board_map['a'] = 0
        self.board_map['b'] = 1
        self.board_map['c'] = 2
        self.board_map['d'] = 3
        self.board_map['e'] = 4
        self.board_map['f'] = 5
        self.board_map['g'] = 6
        self.board_map['h'] = 7

    # Perform a given move
    def move(self, move):
        move = move.lower()
        # assumes format nb1d2
        if self.turn is 'w':
            move = move[0].upper() + move[1:]
        # Check if piece is where it is said to be
        if self.board[int(move[2]) - 1][self.board_map[move[1]]] is move[0]:
            # Move the piece
            self.board[int(move[2]) - 1][self.board_map[move[1]]] = ''
            self.board[int(move[4]) - 1][self.board_map[move[3]]] = move[0]
            # Update turn
            if self.turn is 'w':
                self.turn = 'b'
            else:
                self.turn = 'w'
                self.move_number += 1
            return True
        else:
            return False

    # Reset the chess board
    def reset(self):
        self.__init__()

    # Returns a FEN string corresponding to the board
    def to_string(self):
        to_return = ''
        row_temp = ''
        s_count = 0
        for row in self.board:
            for space in row:
                if space is not '':
                    if s_count is not 0:
                        row_temp += str(s_count)
                        s_count = 0
                    row_temp += space
                else:
                    s_count += 1
            if s_count is not 0:
                row_temp += str(s_count)
                s_count = 0
            to_return = row_temp + '/' + to_return
            row_temp = ''
        to_return = '{0} {1} {2} {3} {4} {5}'.format(to_return[0:-1], self.turn, self.castling, self.en_passant,
                                                     str(self.half_clock), str(self.move_number))
        return to_return


class EmojiChess(Chess):

    def __init__(self):
        self.emoji_map = {}
        super().__init__()

    def construct(self):
        super().construct()
        self.emoji_map['P'] = '\U0001F476\U0001F3FB'
        self.emoji_map['R'] = '\U0001F44A\U0001F3FB'
        self.emoji_map['N'] = '\U0001F984'
        self.emoji_map['B'] = '\U0001F645\U0001F3FB\U0000200D\U00002642\U0000FE0F'
        self.emoji_map['Q'] = '\U0001F478\U0001F3FB'
        self.emoji_map['K'] = '\U0001F934\U0001F3FB'

        self.emoji_map['p'] = '\U0001F476\U0001F3FF'
        self.emoji_map['r'] = '\U0001F44A\U0001F3FF'
        self.emoji_map['n'] = '\U0001F40E'
        self.emoji_map['b'] = '\U0001F645\U0001F3FF\U0000200D\U00002642\U0000FE0F'
        self.emoji_map['q'] = '\U0001F478\U0001F3FF'
        self.emoji_map['k'] = '\U0001F934\U0001F3FF'

    def emoji_string(self):
        temp = [[], [], [], [], [], [], [], []]
        for r in range(7, -1, -1):
            for c in range(0, 8):
                if self.board[r][c] is '':
                    if (r + c) % 2 is 0:
                        temp[7 - r].append('\U00002B1B')
                    else:
                        temp[7 - r].append('\U00002B1C')
                else:
                    temp[7 - r].append(self.emoji_map[self.board[r][c]])
        to_return = ''
        for r in temp:
            for c in r:
                to_return += c
            to_return += '\n'
        return to_return

    def copy(self):
        pyperclip.copy(self.emoji_string())
