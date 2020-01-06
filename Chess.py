# import subprocess as sp

filnum = {
    'a': 1,
    'b': 2,
    'c': 3,
    'd': 4,
    'e': 5,
    'f': 6,
    'g': 7,
    'h': 8
}
pieces = {
    'white king': '/u2654',
    'white queen': '/u2655',
    'white rook': '/u2656',
    'white bishop': '/u2657',
    'white knight': '/u2658',
    'white pawn': '/u2659',
    'black king': '/u265a',
    'black queen': '/u265b',
    'black rook': '/u265c',
    'black bishop': '/u265d',
    'black knight': '/u265e',
    'black pawn': '/u265f'
}
piecepos = {
    ('e', 1): 'white king',
    ('d', 1): 'white queen',
    ('a', 1): 'Lwhite rook',
    ('h', 1): 'Rwhite rook',
    ('c', 1): 'Lwhite bishop',
    ('f', 1): 'Rwhite bishop',
    ('b', 1): 'Lwhite knight',
    ('g', 1): 'Rwhite knight',
    ('e', 8): 'black king',
    ('d', 8): 'black queen',
    ('a', 8): 'Lblack rook',
    ('h', 8): 'Rblack rook',
    ('c', 8): 'Lblack bishop',
    ('f', 8): 'Rblack bishop',
    ('b', 8): 'Lblack knight',
    ('g', 8): 'Rblack knight'
}
enemies = {
    'white': 'black',
    'black': 'white'
}
Wpawns = set()
Bpawns = set()
selected = []
empty = []


class Piece:
    def __init__(self, name, color):
        self.alive = True
        self.name = name
        self.team = color
        if color == 'white':
            self.direction = 1
        else:
            self.direction = -1


class King(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        enemy = set()
        for rnk, fil in piecepos:
            if enemies[self.team] in piecepos[(rnk, fil)]:
                enemy.add((rnk, fil))
        available = empty + enemy
        for rnk, fil in available:
            if abs(rnk - coor[0]) <= 1 and abs(filnum[fil] - filnum[coor[1]]) <= 1:  # noqa: E501
                if not (rnk, fil) == coor:
                    validmoves.add((rnk, fil))
        return validmoves


class Queen(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        for rnk, fil in empty:
            if abs(rnk - coor[0]) == abs(filnum[fil] - filnum[coor[1]]):
                validmoves.add((rnk, fil))
            elif rnk == coor[0] or fil == coor[1]:
                validmoves.add((rnk, fil))
        return validmoves


class Rook(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        for rnk, fil in empty:
            if rnk == coor[0] or fil == coor[1]:
                validmoves.add((rnk, fil))
        return validmoves


class Bishop(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        for rnk, fil in empty:
            if abs(rnk - coor[0]) == abs(filnum[fil] - filnum[coor[1]]):
                validmoves.add((rnk, fil))
        return validmoves


class Knight(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        for rnk, fil in empty:
            if abs(rnk - coor[0]) == 2 and abs(filnum[fil] - filnum[coor[1]]) == 1:  # noqa: E501
                validmoves.add((rnk, fil))
            elif abs(rnk - coor[0]) == 1 and abs(filnum[fil] - filnum[coor[1]]) == 2:  # noqa: E501
                validmoves.add((rnk, fil))
        return validmoves


class Pawn(Piece):
    def can_move_to(self, coor):
        validmoves = {(coor[0] + 1, coor[1] + self.team), (coor[0] - 1, coor[1] + self.team)}  # noqa: E501
        for rnk, fil in empty:
            if (rnk, fil) in validmoves:
                validmoves.remove((rnk, fil))
            if rnk - coor[0] == 1 * self.team:
                validmoves.add((rnk, fil))
        return validmoves


def make_board():
    for rnk in '87654321':
        rnk = int(rnk)
        print(rnk)
        for fil in 'abcdefgh':
            if (rnk, fil) in empty:
                print('   ')
            elif (rnk, fil) in selected:
                print(' /u2022 ')
            elif (rnk, fil) in Wpawns:
                print(pieces['white pawn'])
            elif (rnk, fil) in Bpawns:
                print(pieces['black pawn'])
            elif (rnk, fil) in piecepos:
                print(piecepos[(rnk, fil)])
            if not fil == 'h':
                print('|')


def take_piece(location):
    del(piecepos[location])


for fil in 'abcdefgh':
    Wpawns.add((2, fil))
    Bpawns.add((7, fil))
for rnk in '6543':
    rnk = int(rnk)
    for fil in 'abcdefgh':
        empty.append((rnk, fil))
