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
enemies = {
    'white': 'black',
    'black': 'white'
}
Wpawns = set()
Bpawns = set()
selectedavailable = []
empty = set()


class Game:
    def __init__(self):
        self.board = self.build_board()
    
    def turn(self):
        pass # TODO write function including select and move functions
    
    @staticmethod
    def build_board():
        piecepos = {
            (1, 'e'): King('white'),
            (1, 'd'): Queen('white'),
            (1, 'a'): Rook('white'),
            (1, 'h'): Rook('white'),
            (1, 'c'): Bishop('white'),
            (1, 'f'): Bishop('white'),
            (1, 'b'): Knight('white'),
            (1, 'g'): Knight('white'),
            (8, 'e'): King('black'),
            (8, 'd'): Queen('black'),
            (8, 'a'): Rook('black'),
            (8, 'h'): Rook('black'),
            (8, 'c'): Bishop('black'),
            (8, 'f'): Bishop('black'),
            (8, 'b'): Knight('black'),
            (8, 'g'): Knight('black')
        }
        for fil in 'abcdefgh':
            piecepos[(2, fil)] = Pawn('white', piecepos)
            piecepos[(7, fil)] = Pawn('black', piecepos)
        return piecepos
    
    def move(self, curr_pos, new_pos):
        try:
            piece = self.board[curr_pos]
        except KeyError:
            return False
        self.board[new_pos] = piece
        del self.board[curr_pos]
        return True


class Piece:
    def __init__(self, color):
        self.color = color
        if color == 'white':
            self.direction = 1
        else:
            self.direction = -1


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2654'
        else:
            self.symbol = '\u265a'

    def can_move_to(self, pos, pieces):
        validmoves = set()
        inrnk, infil = pos
        for rnk in range(inrnk - 1, inrnk + 1):
            for fil in range(filnum[infil] - 1, filnum[infil] + 1):
                fil = ' abcdefgh'[fil]
                if (rnk, fil) in pieces:
                    if pieces[(rnk, fil)].color == self.color:
                        pass
                    elif rnk in range(1,8) and fil in 'abcdefgh':
                        pass
                    else:
                        validmoves.add((rnk, fil))
                else:
                    validmoves.add((rnk, fil))
        return validmoves


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2655'
        else:
            self.symbol = '\u265b'

    def can_move_to(self, pos, pieces):
        validmoves = set()
        inrnk, infil = pos
        for x in (-7, 7):
            for rnk in range(inrnk, inrnk + x):
                if rnk not in range(1, 8):
                    break
                elif (rnk, infil) in pieces:
                    if pieces[(rnk, infil)].color == self.color:
                        break
                else:
                    validmoves.add((rnk, infil))
            for fil in range(filnum[infil], filnum[infil] + x):
                fil = ' abcdefgh'[fil]
                if fil not in range(1, 8):
                    break
                elif (inrnk, ' abcdefgh'[fil]) in pieces:
                    if pieces[(inrnk, ' abcdefgh'[fil])].color == self.color:
                        break
                else:
                    validmoves.add((inrnk, ' abcdefgh'[fil]))
        return validmoves # TODO add diagonal path


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2656'
        else:
            self.symbol = '\u265c'

    def can_move_to(self, pos, pieces):
        validmoves = set()
        inrnk, infil = pos
        for x in (-7, 7):
            for rnk in range(inrnk, inrnk + x):
                if rnk not in range(1, 8):
                    break
                elif (rnk, infil) in pieces:
                    if pieces[(rnk, infil)].color == self.color:
                        break
                else:
                    validmoves.add((rnk, infil))
            for fil in range(filnum[infil], filnum[infil] + x):
                fil = ' abcdefgh'[fil]
                if fil not in range(1, 8):
                    break
                elif (inrnk, ' abcdefgh'[fil]) in pieces:
                    if pieces[(inrnk, ' abcdefgh'[fil])].color == self.color:
                        break
                else:
                    validmoves.add((inrnk, ' abcdefgh'[fil]))
        return validmoves


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2657'
        else:
            self.symbol = '\u265d'

    def can_move_to(self, pos, pieces):
        validmoves = set()
        enemy = set()
        for rnk, fil in pieces:
            if pieces[(rnk, fil)].color in enemies[self.color]:
                enemy.add((rnk, fil))
        if self.color == 'white':
            pawns = Bpawns
        else:
            pawns = Wpawns
        available = empty.union(enemy.union(pawns))
        for rnk, fil in available:
            if abs(rnk - pos[0]) == abs(filnum[fil] - filnum[pos[1]]):
                validmoves.add((rnk, fil))
        return validmoves


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2658'
        else:
            self.symbol = '\u265e'

    def can_move_to(self, pos, pieces):
        validmoves = set()
        inrnk, infil = pos
        infil = filnum[infil]
        for x in (-2, 2):
            for y in (-1, 1):
                validmoves.add((inrnk + x, ' abcdefgh'[infil + y]))
                validmoves.add((inrnk + y, ' abcdefgh'[infil + x]))
        for rnk, fil in validmoves:
            if (rnk, fil) in pieces:
                if pieces[(rnk, fil)].color == self.color:
                    validmoves.remove((rnk, fil))
            elif rnk not in range(1, 8) or fil not in 'abcdefgh':
                validmoves.remove((rnk, fil))
        return validmoves


class Pawn(Piece):
    def __init__(self, color, pieces):
        super().__init__(color)
        if color == 'white':
            self.symbol = '\u2659'
        else:
            self.symbol = '\u265e'

    def can_move_to(self, pos, pieces):
        validmoves = {(pos[0] + 1, pos[1] + self.color), (pos[0] - 1, pos[1] + self.color)}  # noqa: E501
        inrnk, infil = pos
        for rnk, fil in validmoves:
            if (rnk, fil) in empty:
                validmoves.remove((rnk, fil))
            elif (rnk, fil) in pieces:
                if pieces[(rnk, fil)].color == self.color:
                    validmoves.remove((rnk, fil))
        move = (inrnk + 1 * self.color, infil)
        if move in empty:
            pass
        elif pieces[(move)].color == self.color:
            pass
        else:
            validmoves.add((rnk, fil))
        return validmoves


def draw_board(pieces):
    for rnk in '87654321':
        rnk = int(rnk)
        print(rnk, end='')
        for fil in 'abcdefgh':
            if (rnk, fil) in empty:
                print('   ', end='')
            elif (rnk, fil) in selectedavailable:
                print(' \u2022 ', end='')
            elif (rnk, fil) in Wpawns:
                print(' ' + '\u2659' + ' ', end='')
            elif (rnk, fil) in Bpawns:
                print(' ' + '\u265f' + ' ', end='')
            elif (rnk, fil) in pieces:
                print(' ' + pieces[(rnk, fil)].symbol, end=' ')
            if not fil == 'h':
                print('|', end='')
            else:
                print('\n', end='')
        if rnk > 1:
            print(' -------------------------------')
        else:
            print('  a   b   c   d   e   f   g   h ')


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


for fil in 'abcdefgh':
    Wpawns.add((2, fil))
    Bpawns.add((7, fil))
for rnk in '6543':
    rnk = int(rnk)
    for fil in 'abcdefgh':
        empty.add((rnk, fil))
#while True: TODO rebuild in board object
#    sp.call('clear', shell=True)
#    draw_board()
#    print('Enter a piece to move')
#    entered = get_input()
#    selectedavailable = piecepos[entered].can_move_to(entered)
#    print('Enter the spot you want to move to, or a different piece: ')
#    entered = get_input()
#    if entered in selectedavailable:
#        move(old, entered)
#    else:
#        selectedavailable = piecepos[entered].can_move_to(entered)