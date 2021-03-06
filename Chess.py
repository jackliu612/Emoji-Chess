# Chess class for logic etc
# Author: Jack Liu
# 12/27/2019
import pyperclip
import re
from PIL import Image


class Chess:
    board_map = {}
    imageDict = {}

    # Constructor
    def __init__(self, bColor=(0, 0, 0), wColor=(255, 255, 255), pieceSet='pieces.png'):
        self.board = []
        self.turn = 'w'
        self.castling = 'KQkq'
        self.en_passant = '-'
        self.half_clock = 0
        self.move_number = 1
        self.bColor = bColor
        self.wColor = wColor
        self.pieceSet = pieceSet
        self.construct()

    # Helper method for constructor
    def construct(self):
        self.createBoard((0, 0, 0), (255, 255, 255))
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

    # Creates the base board image given two colors
    def createBoard(self):
        board = Image.new('RGBA', (64 * 8, 64 * 8), self.bColor)
        whiteSquare = Image.new('RGB', (64, 64), self.wColor)
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 0:
                    board.paste(whiteSquare, (r * 64, c * 64, (r + 1) * 64, (c + 1) * 64))
        return board

    # Creates an image dictionary for all the piece images
    def createImageDict(self):
        pieces = Image.open(self.pieceSet)
        # White Pieces
        self.imageDict['K'] = pieces.crop((0, 64, 64, 128))
        self.imageDict['Q'] = pieces.crop((64, 64, 128, 128))
        self.imageDict['R'] = pieces.crop((128, 64, 192, 128))
        self.imageDict['N'] = pieces.crop((192, 64, 256, 128))
        self.imageDict['B'] = pieces.crop((256, 64, 320, 128))
        self.imageDict['P'] = pieces.crop((320, 64, 384, 128))
        # Black Pieces
        self.imageDict['k'] = pieces.crop((0, 0, 64, 64))
        self.imageDict['q'] = pieces.crop((64, 0, 128, 64))
        self.imageDict['r'] = pieces.crop((128, 0, 192, 64))
        self.imageDict['n'] = pieces.crop((192, 0, 256, 64))
        self.imageDict['b'] = pieces.crop((256, 0, 320, 64))
        self.imageDict['p'] = pieces.crop((320, 0, 384, 64))

    # Perform a given move
    def move(self, move):
        try:
            move = move.lower()
            # assumes format nb1d2
            if self.turn == 'w':
                move = move[0].upper() + move[1:]
            piece = move[0]
            s_row = int(move[2]) - 1
            s_col = self.board_map[move[1]]
            e_row = int(move[4]) - 1
            e_col = self.board_map[move[3]]
            # Check if piece is where it is said to be
            if self.move_helper(piece, s_row, s_col, e_row, e_col):
                # Move the piece
                self.board[s_row][s_col] = ''
                self.board[e_row][e_col] = piece
                # Update turn
                if self.turn == 'w':
                    self.turn = 'b'
                else:
                    self.turn = 'w'
                    self.move_number += 1
                return True
            else:
                return False
        except ValueError:
            return False
        except IndexError:
            return False

    # Helper method which determines if move is valid
    def move_helper(self, piece, s_row, s_col, e_row, e_col):
        if s_row < 0 or s_row > 7 or s_col < 0 or s_col > 7 or e_row < 0 or e_row > 7 or e_col < 0 or e_col > 7 or self.board[s_row][s_col] != piece:
            return False
        if piece.lower() == 'p':
            self.check_pawn(piece, e_row, e_col)
        elif piece.lower() == 'r':
            self.check_rook(piece, e_row, e_col)
        elif piece.lower() == 'n':
            self.check_knight(piece, e_row, e_col)
        elif piece.lower() == 'b':
            return False
        return self.board[s_row][s_col] is piece

    def check_pawn(self, piece, s_row, s_col, e_row, e_col):
        return True

    def check_rook(self, piece, s_row, s_col, e_row, e_col):
        if s_row == e_row:
            for i in range(s_col, e_col):
                if self.board[s_row][i] != '':
                    return False
        elif s_col == e_col:
            for i in range(s_row, e_row):
                if self.board[i][s_col] != '':
                    return False
        else:
            return False
        return self.valid_end(self, e_row, e_col)

    def check_knight(self, piece, s_row, s_col, e_row, e_col):
        if (abs(e_row - s_row) == 2 and abs(e_col - s_col) == 1) or (abs(e_row - s_row) == 2 and abs(e_col - s_col) == 1):
            return self.valid_end(piece, e_row, e_col)
        else:
            return False

    def check_bishop(self, piece, s_row, s_col, e_row, e_col):
        if abs(e_row - s_row) == abs(e_col - s_col):
            direction = (e_col - s_col) / abs(e_col - s_col)
            for i in range(s_row, e_row):
                if self.board[i][s_col + direction * abs(i - s_row)] != '':
                    return False
            return self.valid_end(piece, e_row, e_col)
        else:
            return False

    def check_queen(self, piece, s_row, s_col, e_row, e_col):
        return True

    def check_king(self, piece, s_row, s_col, e_row, e_col):
        return True

    # Helper method to determine if end location is a valid capture or not
    def valid_end(self, piece, e_row, e_col):
        # White piece
        if re.match(r'[PRNBKQ]', piece):
            return re.match(r'[prnbkq ]', self.board[e_row][e_col])
        # Black piece
        else:
            return re.match(r'[PRNBKQ ]', self.board[e_row][e_col])

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
