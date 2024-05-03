class Vector:
    def __init__(self, x, y, color, img, function, score, move):
        self.x = x  # int - float - top left corner's x
        self.y = y  # int / float - top left corner's y
        self.color = color  # str - piece's allegiance (Black - White)
        self.img = img  # surface - img will be displayed on the Screen
        self.function = function  # function - function of a list with the possible places for self
        self.score = score  # int - value of self
        self.move = move  # bool - if player moved or not


def KnightVector(x, y, z):
    ListAppend = [(x + 1, y + 2), (x - 1, y + 2),
                  (x - 1, y - 2),
                  (x + 1, y - 2), (x + 2, y + 1), (x - 2, y + 1),
                  (x - 2, y - 1),
                  (x + 2, y - 1)]

    return ListAppend


def BishopVector(x, y, z):
    ListAppend = [(x + z, y + z), (x - z, y + z),
                  (x + z, y - z), (x - z, y - z)]

    return ListAppend


def RookVector(x, y, z):
    ListAppend = [(x + z, y), (x - z, y),
                  (x, y + z), (x, y - z)]

    return ListAppend


def QueenVector(x, y, z):
    ListAppend = [(x + z, y), (x - z, y),
                  (x, y + z), (x, y - z), (x + z, y + z), (x - z, y + z),
                  (x + z, y - z), (x - z, y - z)]

    return ListAppend


def KingVector(x, y, POINTS):
    ListAppend = [(x + 1, y), (x - 1, y),
                  (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y + 1),
                  (x + 1, y - 1), (x - 1, y - 1)]

    King = pieces[POINTS.index((x, y))]

    if King.color == "White":
        Rook, Rook2 = RookList[0], RookList[1]
    else:
        Rook, Rook2 = RookList[2], RookList[3]

    if not King.move:

        if not Rook2.move:
            if (Rook2.x - 1, Rook2.y) not in POINTS:
                if (Rook2.x - 2, Rook2.y) not in POINTS:
                    ListAppend.append((Rook2.x - 1, Rook.y))

        if not Rook.move:
            if (Rook.x + 3, Rook.y) not in POINTS:
                if (Rook.x + 1, Rook.y) not in POINTS:
                    if (Rook.x + 2, Rook.y) not in POINTS:
                        ListAppend.append((Rook.x + 2, Rook.y))

    return ListAppend


def PawnVectorBlack(x, y, POINTS):
    ListAppend = []

    if (x, y + 1) not in POINTS:
        ListAppend.append((x, y + 1))

        if y == 1 and len(ListAppend) > 0 and (x, y + 2) not in POINTS:
            ListAppend.append((x, y + 2))

    if (x, y) in POINTS:
        if (x + 1, y + 1) in POINTS:
            if pieces[POINTS.index((x + 1, y + 1))].color is not pieces[POINTS.index((x, y))].color:
                ListAppend.append((x + 1, y + 1))

        if (x - 1, y + 1) in POINTS:
            if pieces[POINTS.index((x - 1, y + 1))].color is not pieces[POINTS.index((x, y))].color:
                ListAppend.append((x - 1, y + 1))

    return [ListAppend]


def PawnVectorWhite(x, y, POINTS):
    ListAppend = []

    if (x, y - 1) not in POINTS:
        ListAppend.append((x, y - 1))

        if y == 6 and len(ListAppend) > 0 and (x, y - 2) not in POINTS:
            ListAppend.append((x, y - 2))

    if (x - 1, y - 1) in POINTS:
        if pieces[POINTS.index((x - 1, y - 1))].color is not pieces[POINTS.index((x, y))].color:
            ListAppend.append((x - 1, y - 1))

    if (x + 1, y - 1) in POINTS:
        if pieces[POINTS.index((x + 1, y - 1))].color is not pieces[POINTS.index((x, y))].color:
            ListAppend.append((x + 1, y - 1))

    return [ListAppend]


KnightWhite = Vector(1, 7, "White", None, KnightVector, 3, False)
KnightWhite2 = Vector(6, 7, "White", None, KnightVector, 3, False)

KnightBlack = Vector(1, 0, "Black", None, KnightVector, 3, False)
KnightBlack2 = Vector(6, 0, "Black", None, KnightVector, 3, False)

KnightsList = [KnightWhite, KnightWhite2, KnightBlack, KnightBlack2]

PawnBlackList = []

for i in range(8):
    PawnBlack = Vector(i, 1, "Black", None, PawnVectorBlack, 1, False)
    PawnBlackList.append(PawnBlack)

PawnWhiteList = []

for i in range(8):
    PawnWhite = Vector(i, 6, "White", None, PawnVectorWhite, 1, False)
    PawnWhiteList.append(PawnWhite)

BishopWhite = Vector(2, 7, "White", None, BishopVector, 3, False)
BishopWhite2 = Vector(5, 7, "White", None, BishopVector, 3, False)

BishopBlack = Vector(2, 0, "Black", None, BishopVector, 3, False)
BishopBlack2 = Vector(5, 0, "Black", None, BishopVector, 3, False)

BishopList = [BishopWhite, BishopWhite2, BishopBlack, BishopBlack2]

RookWhite = Vector(0, 7, "White", None, RookVector, 5, False)
RookWhite2 = Vector(7, 7, "White", None, RookVector, 5, False)

RookBlack = Vector(0, 0, "Black", None, RookVector, 5, False)
RookBlack2 = Vector(7, 0, "Black", None, RookVector, 5, False)

RookList = [RookWhite, RookWhite2, RookBlack, RookBlack2]

QueenWhite = Vector(3, 7, "White", None, QueenVector, 9, False)
QueenBlack = Vector(3, 0, "Black", None, QueenVector, 9, False)

QueensList = [QueenWhite, QueenBlack]

KingWhite = Vector(4, 7, "White", None, KingVector, 1000, False)
KingBlack = Vector(4, 0, "Black", None, KingVector, 1000, False)

KingsList = [KingWhite, KingBlack]

Lists = [KnightsList, PawnBlackList, PawnWhiteList, BishopList, RookList, QueensList, KingsList]

pieces = []
for List in Lists:
    for piece in List:
        pieces.append(piece)
