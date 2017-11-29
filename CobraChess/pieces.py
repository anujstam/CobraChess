import sys

symbols = {'R': 'Rook', 'N': 'Knight', 'B': 'Bishop', 'Q': 'Queen', 'K': 'King', 'P': 'Pawn'}


class InvalidPiece(Exception):
    pass


class Invalidcolour(Exception):
    pass


def piece(piece, colour='white'):  # Creates piece instances using symbol; lower-> black and upper -> white
    if piece in (None, ' '):
        return
    if len(piece) == 1:
        if piece.isupper():
            colour = 'white'
        else:
            colour = 'black'
        piece = symbols[piece.upper()]
    thismodule = sys.modules[__name__]  # used cuz this file needs to be imported and some weird stuff happens w/o it
    return thismodule.__dict__[piece](colour)


class Piece(object):
    __slots__ = ('symbol', 'colour')  # This means that a piece object can have only these 2 attributes

    def __init__(self, colour):
        if colour == 'white':
            self.symbol = self.symbol.upper()
        elif colour == 'black':
            self.symbol = self.symbol.lower()

        try:
            self.colour = colour
        except KeyError:
            raise Invalidcolour

    @property
    def name(self):
        return self.__class__.__name__

    def place(self, board):
        self.board = board

    def possible_moves(self, position, orthogonal, diagonal, distance):  # gets all moves
        board = self.board
        legal_moves = []
        orth = ((-1, 0), (0, -1), (0, 1), (1, 0))
        diag = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        piece = self
        from_ = board.number_notation(position)
        if orthogonal and diagonal:
            directions = diag + orth
        elif diagonal:
            directions = diag
        elif orthogonal:
            directions = orth
        for x, y in directions:
            collision = False
            for step in range(1, distance + 1):
                if collision: break
                dest = from_[0] + step * x, from_[1] + step * y
                if self.board.letter_notation(dest) not in board.occupied('white') + board.occupied('black'):
                    legal_moves.append(dest)
                elif self.board.letter_notation(dest) in board.occupied(piece.colour):
                    collision = True
                else:
                    legal_moves.append(dest)
                    collision = True
        legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)

    def __str__(self):  # overriding builtin str
        return self.symbol

    def __repr__(self):  # used to actually give prinatble statements
        return "<" + self.colour.capitalize() + " " + self.__class__.__name__ + ">"


# These are the individual pieces


class Pawn(Piece):
    symbol = 'p'

    def possible_moves(self, position):  # Pawns move too differently so they don't use the same move method
        board = self.board
        position = position.upper()
        piece = self
        if self.colour == 'white':
            homerow, direction, enemy, endrow = 1, 1, 'black', 7
        else:
            homerow, direction, enemy, endrow = 6, -1, 'white', 0
        legal_moves = []
        blocked = board.occupied('white') + board.occupied('black')
        from_ = board.number_notation(position)  # from is a keyword so used from_ instead
        forward = from_[0] + direction, from_[1]
        if board.letter_notation(forward) not in blocked:
            legal_moves.append(forward)
            if from_[0] == homerow:
                # double move if pawn hasn't moved
                double_forward = (forward[0] + direction, forward[1])
                if board.letter_notation(double_forward) not in blocked:
                    legal_moves.append(double_forward)
        for a in range(-1, 2, 2):  # pawn captures on the diagonal
            attack = from_[0] + direction, from_[1] + a
            if board.letter_notation(attack) in board.occupied(enemy):
                legal_moves.append(attack)
        legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)


class Knight(Piece):
    symbol = 'n'

    def possible_moves(self, position):
        board = self.board
        position = position.upper()
        legal_moves = []
        from_ = board.number_notation(position)
        piece = board.get(position)
        # change in positions after jumping
        deltas = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for x, y in deltas:
            dest = from_[0] + x, from_[1] + y
            if (board.letter_notation(dest) not in board.occupied(piece.colour)):
                legal_moves.append(dest)
        legal_moves = filter(board.is_in_bounds, legal_moves)
        return map(board.letter_notation, legal_moves)


class Rook(Piece):
    symbol = 'r'

    def possible_moves(self, position):
        position = position.upper()
        return super(Rook, self).possible_moves(position, True, False, 8)


class Bishop(Piece):
    symbol = 'b'

    def possible_moves(self, position):
        position = position.upper()
        return super(Bishop, self).possible_moves(position, False, True, 8)


class Queen(Piece):
    symbol = 'q'

    def possible_moves(self, position):
        position = position.upper()
        return super(Queen, self).possible_moves(position, True, True, 8)


class King(Piece):
    symbol = 'k'
    move_length = 1

    def possible_moves(self, position):
        position = position.upper()
        return super(King, self).possible_moves(position, True, True, 1)
