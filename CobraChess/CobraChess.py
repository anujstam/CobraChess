# -*- encoding: utf-8 -*-
import os
import sys
import time

import board
import eastereggs
# UNICODE_PIECES = { 'r': u'♜', 'n': u'♞', 'b': u'♝', 'q': u'♛', 'k': u'♚', 'p': u'♟', 'R': u'♖', 'N': u'♘', 'B': u'♗', 'Q': u'♕', 'K': u'♔', 'P': u'♙', None: ' '}

# UNICODE_PIECES = {'k':u'\u265A', "q":u'\u265B','r': u'\u265C',"b": u'\u265D','n':u'\u265E','p':u'\u265F','K':u'\u2654', "Q":u'\u2655','R': u'\u2656',"B": u'\u2657','N':u'\u2658','P':u'\u2659'}

UNICODE_PIECES = {'k': 'k', "q": 'q', 'r': 'r', "b": 'b', 'n': 'n', 'p': 'p', 'K': 'K', "Q": 'Q', 'R': 'R', "B": 'B',
                  'N': 'N', 'P': 'P'}


class BoardGUI(object):
    error = ''

    def __init__(self, chessboard):
        self.board = chessboard

    def move(self):
        os.system("cls")
        self.unicode_representation()
        print("\n", self.error)
        print(">>>", end=" ")
        self.error = ''
        coord = input()
        if coord == "exit":
            print("Thanks for playing!")
            exit(0)
        if coord == "surrender":
            self.endgame()
        if coord[0] == "!":
            eastereggs.eastereggs(coord[1:])
        if coord[0:2] == "cs":
            self.board.castle(coord[len(coord) - 1])
        else:
            try:
                if len(coord) != 4 and coord[0:2] != "cs":
                    raise board.InvalidCoord
                else:
                    self.board.move(coord[0:2], coord[2:4])
                os.system("cls")
            except board.ChessError as error:
                self.error = error.__class__.message

        self.move()

    def endgame(self):
        loser_colour = self.board.player_turn.capitalize()
        colours = ["White", "Black"]
        winner_colour = ""
        for j in colours:
            if j != loser_colour:
                winner_colour = j
        os.system('cls')
        if winner_colour == "White":
            print("""
 _    _ _     _ _         _    _ _             _ 
| |  | | |   (_) |       | |  | (_)           | |
| |  | | |__  _| |_ ___  | |  | |_ _ __  ___  | |
| |/\| | '_ \| | __/ _ \ | |/\| | | '_ \/ __| | |
\  /\  / | | | | ||  __/ \  /\  / | | | \__ \ |_|
 \/  \/|_| |_|_|\__\___|  \/  \/|_|_| |_|___/ (_|
                                                     
                                                     
                                                                            
            """)
            time.sleep(1)
            os.system('cls')
            print("""
 _    _ _     _ _         _    _ _             _ _ 
| |  | | |   (_) |       | |  | (_)           | | |
| |  | | |__  _| |_ ___  | |  | |_ _ __  ___  | | |
| |/\| | '_ \| | __/ _ \ | |/\| | | '_ \/ __| | | |
\  /\  / | | | | ||  __/ \  /\  / | | | \__ \ |_|_|
 \/  \/|_| |_|_|\__\___|  \/  \/|_|_| |_|___/ (_|_|
                                                     
                                                     

                        """)
            time.sleep(1)
            os.system('cls')
            print("""
 _    _ _     _ _         _    _ _             _ _ _ 
| |  | | |   (_) |       | |  | (_)           | | | |
| |  | | |__  _| |_ ___  | |  | |_ _ __  ___  | | | |
| |/\| | '_ \| | __/ _ \ | |/\| | | '_ \/ __| | | | |
\  /\  / | | | | ||  __/ \  /\  / | | | \__ \ |_|_|_|
 \/  \/|_| |_|_|\__\___|  \/  \/|_|_| |_|___/ (_|_|_)
                                                     
                                                     
                        """)
            time.sleep(1)
            os.system('cls')
            sys.exit(0)
        elif winner_colour == "Black":
            print("""
______ _            _      _    _ _             _  
| ___ \ |          | |    | |  | (_)           | |
| |_/ / | __ _  ___| | __ | |  | |_ _ __  ___  | |
| ___ \ |/ _` |/ __| |/ / | |/\| | | '_ \/ __| | |
| |_/ / | (_| | (__|   <  \  /\  / | | | \__ \ |_|
\____/|_|\__,_|\___|_|\_\  \/  \/|_|_| |_|___/ (_|
                                                      
                                                      

                        """)
            time.sleep(1)
            os.system('cls')
            print("""
______ _            _      _    _ _             _ _  
| ___ \ |          | |    | |  | (_)           | | |
| |_/ / | __ _  ___| | __ | |  | |_ _ __  ___  | | |
| ___ \ |/ _` |/ __| |/ / | |/\| | | '_ \/ __| | | |
| |_/ / | (_| | (__|   <  \  /\  / | | | \__ \ |_|_|
\____/|_|\__,_|\___|_|\_\  \/  \/|_|_| |_|___/ (_|_|
                                                      
                                                      
                                    """)
            time.sleep(1)
            os.system('cls')
            print("""
______ _            _      _    _ _             _ _ _ 
| ___ \ |          | |    | |  | (_)           | | | |
| |_/ / | __ _  ___| | __ | |  | |_ _ __  ___  | | | |
| ___ \ |/ _` |/ __| |/ / | |/\| | | '_ \/ __| | | | |
| |_/ / | (_| | (__|   <  \  /\  / | | | \__ \ |_|_|_|
\____/|_|\__,_|\___|_|\_\  \/  \/|_|_| |_|___/ (_|_|_)
                                                      
                                                      
                                    """)
            time.sleep(1)
            os.system('cls')
            sys.exit(0)

    def unicode_representation(self):
        print("\n", ("%s's turn\n" % self.board.player_turn.capitalize()).center(28))
        for number in self.board.axis_x[::-1]:
            print(" " + str(number) + " ", end=" ")
            for letter in self.board.axis_y:
                piece = self.board[letter + str(number)]
                if piece is not None:
                    print(UNICODE_PIECES[piece.symbol] + ' ', end=" ")
                else:
                    print('  ', end=" ")
            print("\n")
        print("    " + "  ".join(self.board.axis_y))


def display(board):
    try:
        gui = BoardGUI(board)
        gui.move()
    except (KeyboardInterrupt, EOFError):
        os.system("cls")
        exit(0)


def introscreen(board):
    print(""" Welcome to CobraChess! 
                            
This is a simple 2 player chess  game. 
Inspired by Liudmil Mitev whose program you can find at https://github.com/liudmil-mitev/Simple-Python-Chess. 
This is my version uses similar concepts but updates them to python 3 ,,adds more features and makes it more robust

                        Key:
                        
White Pieces: Pawn  Rook  Knight  Bishop  Queen  King
                P     R     N       B       Q     K
                
Black Pieces: Pawn  Rook  Knight  Bishop  Queen  King
                p     r     n       b       q     k


State a move in chess notation (e.g. A2A3). Type \"exit\" to leave
Move notation is case insensitive
Type "surrender" to concede defeat
You cannot undo your last move. Think before you move!

                        GLHF!


Press "y" to play or anything else to exit
    """)
    choice = input(">>>")
    if choice == "y":
        display(board)
    else:
        sys.exit(0)


if __name__ == '__main__':
    Chessgame = board.Board()
    introscreen(Chessgame)
