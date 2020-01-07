import subprocess as sp

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
piecepos = {}
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
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if abs(rnk - coor[0]) <= 1 and abs(filnum[fil] - filnum[coor[1]]) <= 1:  # noqa: E501
                if not (rnk, fil) == coor:
                    validmoves.add((rnk, fil))
        return validmoves


class Queen(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        enemy = set()
        for rnk, fil in piecepos:
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if abs(rnk - coor[0]) == abs(filnum[fil] - filnum[coor[1]]):
                validmoves.add((rnk, fil))
            elif rnk == coor[0] or fil == coor[1]:
                validmoves.add((rnk, fil))
        return validmoves


class Rook(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        enemy = set()
        for rnk, fil in piecepos:
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if rnk == coor[0] or fil == coor[1]:
                validmoves.add((rnk, fil))
        return validmoves


class Bishop(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        enemy = set()
        for rnk, fil in piecepos:
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if abs(rnk - coor[0]) == abs(filnum[fil] - filnum[coor[1]]):
                validmoves.add((rnk, fil))
        return validmoves


class Knight(Piece):
    def can_move_to(self, coor):
        validmoves = set()
        enemy = set()
        for rnk, fil in piecepos:
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if abs(rnk - coor[0]) == 2 and abs(filnum[fil] - filnum[coor[1]]) == 1:  # noqa: E501
                validmoves.add((rnk, fil))
            elif abs(rnk - coor[0]) == 1 and abs(filnum[fil] - filnum[coor[1]]) == 2:  # noqa: E501
                validmoves.add((rnk, fil))
        return validmoves


class Pawn(Piece):
    def can_move_to(self, coor):
        validmoves = {(coor[0] + 1, coor[1] + self.team), (coor[0] - 1, coor[1] + self.team)}  # noqa: E501
        enemy = set()
        for rnk, fil in piecepos:
            if piecepos[(rnk, fil)].team in enemies[self.team]:
                enemy.add((rnk, fil))
        if self.team == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty + enemy + pawns
        for rnk, fil in available:
            if (rnk, fil) in empty:
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
        if rnk > 1:
            print('-------------------------------')


def move(oldcoor, newcoor):
    if newcoor in piecepos:
        del(piecepos[newcoor])
    piecepos[newcoor] = piecepos[oldcoor]
    del(piecepos[oldcoor])


def validate(item, rnkorfil):
    if rnkorfil:
        if item > 8:
            validate(input('Number too big, enter again: '), True)
        if item < 1:
            validate(input('Number too small, enter again: '), True)
    else:
        if not item.isalpha:
            validate(input('Invalid character, enter again: '), False)
        if item not in 'abcdefgh':
            validate(input('Letter out of range, enter again: '), False)
    return item

def get_input():
    while True:
        try:
            rnkchoose = int(input('Choose a rank: '))
            break
        except TypeError:
            print('Invalid character')
    rnkchoose = validate(rnkchoose, True)
    filchoose = validate(input('Choose a file: '), False)
    return (rnkchoose, filchoose)
    

piecepos = {
    ('e', 1): King('white king', 'white'),
    ('d', 1): Queen('white queen', 'white'),
    ('a', 1): Rook('Lwhite rook', 'white'),
    ('h', 1): Rook('Rwhite rook', 'white'),
    ('c', 1): Bishop('Lwhite bishop', 'white'),
    ('f', 1): Bishop('Rwhite bishop', 'white'),
    ('b', 1): Knight('Lwhite knight', 'white'),
    ('g', 1): Knight('Rwhite knight', 'white'),
    ('e', 8): King('black king', 'black'),
    ('d', 8): Queen('black queen', 'black'),
    ('a', 8): Rook('Lblack rook', 'black'),
    ('h', 8): Rook('Rblack rook', 'black'),
    ('c', 8): Bishop('Lblack bishop', 'black'),
    ('f', 8): Bishop('Rblack bishop', 'black'),
    ('b', 8): Knight('Lblack knight', 'black'),
    ('g', 8): Knight('Rblack knight', 'black')
}

for fil in 'abcdefgh':
    Wpawns.add((2, fil))
    Bpawns.add((7, fil))
for rnk in '6543':
    rnk = int(rnk)
    for fil in 'abcdefgh':
        empty.append((rnk, fil))
while True:
    sp.call('clear', shell=True)