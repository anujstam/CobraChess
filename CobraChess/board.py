import re
from copy import deepcopy

import pieces


# Handling possible errors through a ChessError exception


class ChessError(Exception):
    pass


class InvalidCoord(ChessError):
    message = "Those coordinates are invalid! "
    pass


class Invalidcolour(ChessError):
    message = "That's the wrong colour!"
    pass


class InvalidMove(ChessError):
    message = "That move isn't allowed"
    pass


class Check(ChessError):
    message = "Your king is under check. You can't make that move"
    pass


class CheckMate(ChessError):
    message = "Checkmate!"
    pass


class Draw(ChessError):
    pass


class NotYourTurn(ChessError):
    message = "Hey! Its not your turn yet!"
    pass


class CantCastle(ChessError):
    message = "Sorry! You cannot castle like this!"
    pass


class InvalidPiece(ChessError):
    message = "Sorry! This is not a valid Piece! Use standard notation"

class InvalidUpgrade(ChessError):
    message = "Sorry! You cannot upgrade to this piece "


FEN_STARTING = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
RANK_REGEX = re.compile(r"^[A-H][1-8]$")  # Dank way of expressing the coordinate system

#legit fem : 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

class Board(dict):  # Class for the chessboard

    axis_y = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
    axis_x = tuple(range(1, 9))  # (1,2,3,...8)

    captured_pieces = {'white': [], 'black': []}
    player_turn = None
    castling = '-'
    en_passant = '-'
    halfmove_clock = 0
    fullmove_number = 1
    history = []

    whitecastle = False
    whitekmove = False
    whitermove = [False, False]
    whitecheck = False

    blackkcastle = False
    blackkmove = False
    blackrmove = [False, False]
    blackcheck = False

    def __init__(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.clear()
        fen = fen.split(' ')

        def expand(match):
            return ' ' * int(match.group(0))

        fen[0] = re.compile(r'\d').sub(expand, fen[0])
        for x, row in enumerate(fen[0].split('/')):
            for y, letter in enumerate(row):
                if letter == ' ':
                    continue
                coord = self.letter_notation((7 - x, y))
                self[coord] = pieces.piece(letter)
                self[coord].place(self)
        if fen[1] == 'w':
            self.player_turn = 'white'
        else:
            self.player_turn = 'black'
        self.castling = fen[2]
        self.en_passant = fen[3]
        self.halfmove_clock = int(fen[4])
        self.fullmove_number = int(fen[5])

    def __getitem__(self, coord):
        if isinstance(coord, str):
            coord = coord.upper()
            if not re.match(RANK_REGEX, coord.upper()):
                raise InvalidCoord
        elif isinstance(coord, tuple):
            coord = self.letter_notation(coord)
        try:
            return super(Board, self).__getitem__(coord)
        except KeyError:
            return None

    def is_in_check_after_move(self, p1, p2):
        # Create a temporary board
        tmp = deepcopy(self)
        tmp._do_move(p1, p2)
        return tmp.is_in_check(self[p1].colour)

    def move(self, p1, p2):
        p1, p2 = p1.upper(), p2.upper()
        piece = self[p1]
        dest = self[p2]

        if piece is None:
            raise InvalidMove
        if self.player_turn != piece.colour:
            raise NotYourTurn("Not " + piece.colour + "'s turn!")

        enemy = self.get_enemy(piece.colour)
        possible_moves = piece.possible_moves(p1)
        # 0. Check if p2 is in the possible moves
        if p2 not in possible_moves:
            raise InvalidMove

        # If enemy has any moves look for check
        if self.all_possible_moves(enemy):
            if self.is_in_check_after_move(p1, p2):
                raise Check

        if not possible_moves and self.is_in_check(piece.colour):
            raise CheckMate
        elif not possible_moves:
            raise Draw
        else:
            self._do_move(p1, p2)
            self._finish_move(piece, dest, p1, p2)

    def castle(self, d):
        self.no_obstacle = True
        if not self.is_in_check(self.player_turn):
            if self.player_turn == 'white':
                if d == "r'":
                    piece = self["H1"]
                    if isinstance(piece, pieces.Rook):
                        for i in ["F", "G"]:
                            if self[i + str(1)] is not None:
                                self.no_obstacle = False
                    if self.whitekmove == False and self.whitermove[1] == False and self.no_obstacle == True and self.whitecheck == False:
                        self["G1"], self["E1"] = self["E1"], self["G1"]
                        self['F1'], self['H1'] = self['H1'], self['F1']
                    else:
                        raise CantCastle

                if d == "l'":
                    piece = self["A1"]
                    if isinstance(piece, pieces.Rook):
                        for i in ["B", "C", "D"]:
                            if self[i + str(1)] is not None:
                                self.no_obstacle = False
                    if self.whitekmove == False and self.whitermove[0] == False and self.no_obstacle == True and self.whitecheck == False:
                        self["A1"], self["D1"] = self["D1"], self["A1"]
                        self['C1'], self['E1'] = self['E1'], self['C1']
                    else:
                        raise CantCastle

            if self.player_turn == 'black':
                if d == "r'":
                    piece = self["H8"]
                    if isinstance(piece, pieces.Rook):
                        for i in ["F", "G"]:
                            if self[i + str(1)] is not None:
                                self.no_obstacle = False
                    if self.blackkmove == False and self.blackrmove[1] == False and self.no_obstacle == True and self.blackcheck == False:
                        self["G8"], self["E8"] = self["E8"], self["G8"]
                        self['F8'], self['H8'] = self['H8'], self['F8']
                    else:
                        raise CantCastle
                if d == "l'":
                    piece = self["A8"]
                    if isinstance(piece, pieces.Rook):
                        for i in ["B", "C", "D"]:
                            if self[i + str(1)] is not None:
                                self.no_obstacle = False
                    if self.blackkmove == False and self.blackrmove[0] == False and self.no_obstacle == True and self.blackcheck == False:
                        self["A8"], self["D8"] = self["D8"], self["A8"]
                        self['C8'], self['E8'] = self['E8'], self['C8']
                    else:
                        raise CantCastle
        else:
            raise CantCastle

    def get_enemy(self, colour):
        if colour == "white":
            return "black"
        else:
            return "white"

    def _do_move(self, p1, p2):  # Doesn't check validity
        piece = self[p1]
        del self[p1]
        self[p2] = piece

    def _finish_move(self, piece, dest, p1, p2):
        enemy = self.get_enemy(piece.colour)
        if piece.colour == 'black':
            self.fullmove_number += 1
        self.halfmove_clock += 1
        self.player_turn = enemy
        abbr = piece.symbol
        if abbr == 'P':
            abbr = ''
            self.halfmove_clock = 0
        if dest is None:
            movetext = abbr + p2.lower()
        else:
            movetext = abbr + 'x' + p2.lower()
            self.halfmove_clock = 0
        if isinstance(piece, pieces.King):
            if piece.colour == 'white':
                self.whitekmove = True
            if piece.colour == 'black':
                self.blackkmove = True

        if isinstance(piece, pieces.Rook):
            if piece.colour == 'white':
                if p1 == "H1":
                    self.whitermove[1] = True
                elif p1 == "A1":
                    self.whitermove[0] = True
            if piece.colour == 'black':
                if p1 == "H8":
                    self.blackrmove[1] = True
                elif p1 == "H1":
                    self.blackrmove[0] = True
        if isinstance(piece, pieces.Pawn):
            new_piece = ""
            if piece.colour == "white":
                if p2[1] == "8":
                    while new_piece == "":
                        new_piece = input("Your pawn has reached the other end! Upgrade to: ").upper()
                        if new_piece not in ["P","R","N", "B", "Q"]:
                            new_piece=""
                            print("Enter a valid upgrade!")
                    self[p2] = pieces.piece(new_piece.upper())
                    self[p2].place(self)

            if piece.colour == "black":
                if p2[1] == "1":
                    while new_piece == "":
                        new_piece = input("Your pawn has reached the other end! Upgrade to: ").lower()
                        if new_piece not in ["p","r","n", "b", "q"]:
                            new_piece=""
                            print("Enter a valid upgrade!")
                    self[p2] = pieces.piece(new_piece.lower())
                    self[p2].place(self)

        self.history.append(movetext)

    def all_possible_moves(self, colour):
        if colour not in ("black", "white"):
            raise Invalidcolour
        result = []
        for coord in self.keys():
            if (self[coord] is not None) and self[coord].colour == colour:
                moves = self[coord].possible_moves(coord)
                if moves:
                    result += moves
        return result

    def occupied(self, colour):
        result = []
        if (colour not in ("black", "white")):
            raise Invalidcolour

        for coord in self:
            if self[coord].colour == colour:
                result.append(coord)
        return result

    def is_king(self, piece):
        return isinstance(piece, pieces.King)

    def get_king_position(self, colour):
        for pos in self.keys():
            if self.is_king(self[pos]) and self[pos].colour == colour:
                return pos

    def get_king(self, colour):
        if (colour not in ("black", "white")):
            raise Invalidcolour
        return self[self.get_king_position(colour)]

    def is_in_check(self, colour):
        if colour not in ("black", "white"):
            raise Invalidcolour
        king = self.get_king(colour)
        enemy = self.get_enemy(colour)
        return king in map(self.__getitem__, self.all_possible_moves(enemy))

    def letter_notation(self, coord):
        if not self.is_in_bounds(coord):
            return
        try:
            return self.axis_y[coord[1]] + str(self.axis_x[coord[0]])
        except IndexError:
            raise InvalidCoord

    def number_notation(self, coord):
        return int(coord[1]) - 1, self.axis_y.index(coord[0])

    def is_in_bounds(self, coord):
        if coord[1] < 0 or coord[1] > 7 or \
                        coord[0] < 0 or coord[0] > 7:
            return False
        else:
            return True
