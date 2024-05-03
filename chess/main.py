import pygame
import random

import math

from settings import *
from buttons import *

# Screen Settings
pygame.mixer.get_init()
pygame.init()

ScreenWidth, ScreenHeight = 630, 630

Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
pygame.display.set_caption("Chess")

FPS = 60
clock = pygame.time.Clock()

# Colors
Yellow = (125, 125, 0)
Grey = (100, 100, 255)

BLACK = (0, 0, 0)
WHITE = (192, 192, 192)

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
Magenta = (255, 0, 255)
Cyan = (0, 255, 255)
Blueish = (0, 0, 128)
Greyish = (100, 120, 92)
white = (255, 255, 255)

# Color List for Color Wheel
ColorList = [Grey,
             BLACK,
             WHITE,
             GREEN,
             RED,
             BLUE,
             YELLOW,
             Magenta,
             Cyan,
             Blueish,
             white]

# Main Menu Buttons Img According to self.img attribute from buttons.py
# --------------------------------------------------------------------------------
ClockImg = pygame.transform.scale(pygame.image.load("assets/RapidClock.PNG").convert(),
                                  (ScreenWidth / 15, ScreenHeight / 15))

BulletImg = pygame.transform.scale(pygame.image.load("assets/BulletImg.PNG").convert(),
                                   (ScreenWidth / 15, ScreenHeight / 15))

BlitzImg = pygame.transform.scale(pygame.image.load("assets/BlitzImg.PNG").convert(),
                                  (ScreenWidth / 15, ScreenHeight / 15))

ReturnButton = pygame.transform.scale(pygame.image.load("assets/BlitzImg.PNG").convert(),
                                      (ScreenWidth / 15, ScreenHeight / 15))
# --------------------------------------------------------------------------------

# Lists of button attribute - time.
# First in tuple is string obj which will be shown on screen, Second in tuple is the integer obj in minutes
# --------------------------------------------------------------------------------

Bullet = [("0 : 10", 0.16667), ("0 : 30", 0.5), ("1 : 00", 1)]
Blitz = [("3 : 00", 3), ("5 : 00", 5)]
Rapid = [("10 : 00", 10), ("15 : 00", 15), ("30 : 00", 30), ("60 : 00", 60)]

TimeList = [Bullet, Blitz, Rapid]
# --------------------------------------------------------------------------------

# List of All Buttons
ButtonList = []

# Time Buttons
# --------------------------------------------------------------------------------
for List in TimeList:

    # place of a time list in the main TimeList
    I = TimeList.index(List)
    for Time in List:
        # place of a time in the time list
        i = List.index(Time)

        Button = Buttons(WHITE, ScreenWidth * (i + 0.25) // 5, ScreenHeight * (I + 1.2) // 4.5, ScreenWidth // 6,
                         ScreenHeight // 11, Time[0], 1, Time[1])

        ButtonList.append(Button)
# --------------------------------------------------------------------------------

# Mode Buttons
Button960 = Buttons(WHITE, ScreenWidth // 15, ScreenHeight // 15, ScreenWidth // 3, ScreenHeight // 11, "960", 0, None)
ButtonNormal = Buttons(WHITE, 9 * ScreenWidth // 15, ScreenHeight // 15, ScreenWidth // 3, ScreenHeight // 11, "Normal",
                       0, None)

ButtonList.append(Button960)
ButtonList.append(ButtonNormal)

# settings Buttons
# -----------------------------------------

HelperButton = Buttons(GREEN, 3.7 * ScreenWidth // 5, ScreenHeight // 1.7, 35, 10, "Yes", 2, None)
HelperButton1 = Buttons(GREEN, 4.2 * ScreenWidth // 5, ScreenHeight // 1.7, 35, 10, "No", 2, None)

ButtonList.append(HelperButton)
ButtonList.append(HelperButton1)

# -----------------------------------------

# Start Game Button
MainButton = Buttons(WHITE, ScreenWidth // 10, 7.5 * ScreenHeight // 9, 8 * ScreenWidth // 10, ScreenHeight // 9,
                     "Play", -1, None)

ButtonList.append(MainButton)

# List of the Game Mode, Game Time and Game Helper. they are = None, before they are selected on the Main Menu
ButtonType = [None, None, None]


# images to Piece's Attribute of img (Chess_Settings.py, self.img)

KnightBlack.img = KnightBlack2.img = pygame.transform.scale(
    pygame.image.load("assets/KnightBlack.jpg").convert(),
    (ScreenWidth / 10, ScreenWidth / 10))

KnightWhite2.img = KnightWhite.img = pygame.transform.scale(
    pygame.image.load("assets/KnightWhite.jpg").convert(), (ScreenWidth / 10, ScreenHeight / 10))

RookWhite.img = RookWhite2.img = pygame.transform.scale(
    pygame.image.load("assets/RookWhite.png").convert(),
    (ScreenWidth / 10, ScreenHeight / 10))

RookBlack.img = RookBlack2.img = pygame.transform.scale(
    pygame.image.load("assets/RookBlack.png").convert(),
    (ScreenWidth / 11, ScreenHeight / 11))

BishopWhite.img = BishopWhite2.img = pygame.transform.scale(
    pygame.image.load("assets/BishopWhite.png").convert(),
    (ScreenWidth / 10, ScreenHeight / 10))

BishopBlack.img = BishopBlack2.img = pygame.transform.scale(
    pygame.image.load("assets/BishopBlack.jpg").convert(),
    (ScreenWidth / 10, ScreenHeight / 10))

QueenBlack.img = pygame.transform.scale(pygame.image.load("assets/QueenBlack.png").convert(),
                                        (ScreenWidth / 9.5, ScreenHeight / 9.5))

QueenWhite.img = pygame.transform.scale(pygame.image.load("assets/QueenWhite.png").convert(),
                                        (ScreenWidth / 9.5, ScreenHeight / 9.5))

KingBlack.img = pygame.transform.scale(pygame.image.load("assets/KingBlack.png").convert(),
                                       (ScreenWidth / 9, ScreenHeight / 9))

KingWhite.img = pygame.transform.scale(pygame.image.load("assets/KingWhite.png").convert(),
                                       (ScreenWidth / 9, ScreenHeight / 9))

for pawn in PawnBlackList:
    pawn.img = pygame.transform.scale(pygame.image.load("assets/PawnBlack.png").convert(),
                                      (ScreenWidth / 11.5, ScreenHeight / 11.5))

for pawn in PawnWhiteList:
    pawn.img = pygame.transform.scale(pygame.image.load("assets/PawnWhite.png").convert(),
                                      (ScreenWidth / 11.5, ScreenHeight / 11.5))


def main():
    def MainMenu(Button: Buttons, X: int, Y: int):

        # button events
        if Buttons.Hover(Button, X, Y):

            if Button.color == WHITE:
                Button.color = GREEN

            if pygame.mouse.get_pressed()[0]:
                if Button.color == GREEN:
                    if Button == MainButton:
                        if None not in ButtonType:
                            Button.color = BLUE

                    else:
                        Button.color = BLUE
                        if ButtonType[Button.type] is not None:
                            ButtonType[Button.type].color = WHITE

                        ButtonType[Button.type] = Button

        elif Button.color == GREEN:
            Button.color = WHITE

    def DrawButton(Button: Buttons):

        pygame.draw.rect(Screen, Button.color, ((Button.x, Button.y), (Button.width, Button.height)), 0, 10)

        ButtonText = font.render(Button.text, True, BLACK, Button.color)
        Screen.blit(ButtonText, ((2 * Button.x + Button.width - ButtonText.get_width()
                                  ) // 2, (2 * Button.y + Button.height - ButtonText.get_height()
                                           ) // 2))

    def DrawBoard(RawColor: tuple, ColColor: tuple):

        """
        Drawing Board
        :param RawColor: tuple
        :param ColColor: tuple
        :return: pass
        """

        # changing color of the board to Row color so there want be cracks in the board
        Screen.fill(RowColor)

        for r in range(0, 8):
            for c in range(0, 8):
                if (c + r) % 2:  # if square is odd
                    PaintWith = ColColor
                else:
                    PaintWith = RawColor

                # drawing squares
                pygame.draw.rect(Screen, PaintWith,
                                 ((r * ScreenWidth // 8, c * ScreenHeight // 8), (ScreenWidth // 8, ScreenHeight // 8)))

    def NumberTransfer(X: float):
        """
        Float to int Function
        :param X: float
        :return: An Integer
        """
        if X - 0.5 > int(X):
            X = int(X) + 1
        else:
            X = int(X)
        return X

    # if Game Mode is 960
    def Mode960():
        List = [0, 1, 2, 3, 4, 5, 6, 7]
        random.shuffle(List)

        # scrambling piece's x
        # -----------------------------------------

        RookWhite.x = RookBlack.x = List[0]
        RookWhite2.x = RookBlack2.x = List[1]

        BishopWhite2.x = BishopBlack2.x = List[2]
        BishopBlack.x = BishopWhite.x = List[3]

        KnightWhite2.x = KnightBlack2.x = List[4]
        KnightBlack.x = KnightWhite.x = List[5]

        QueenWhite.x = QueenBlack.x = List[6]

        KingWhite.x = KingBlack.x = List[7]
        # -----------------------------------------

        # unable Castle
        KingWhite.move = False
        KingBlack.move = False

    def action(ChosenPiece, POINTS):
        """

        :param ChosenPiece: piece chosen
        :param POINTS: all pieces locations
        :return: all possible points for chosen piece
        """

        VectorList = []
        IndexList = []
        Point = []

        if ChosenPiece.function == PawnVectorBlack or ChosenPiece.function == PawnVectorWhite:
            return ChosenPiece.function(ChosenPiece.x, ChosenPiece.y, POINTS)

        for z in range(1, 9):

            if ChosenPiece.function == KingVector:
                ListAppend = ChosenPiece.function(ChosenPiece.x, ChosenPiece.y, POINTS)
            else:
                ListAppend = ChosenPiece.function(ChosenPiece.x, ChosenPiece.y, z)

            for PossiblePoint in ListAppend:
                if 0 <= PossiblePoint[0] <= 7 and 0 <= PossiblePoint[1] <= 7:  # if in borders of the game
                    if PossiblePoint in POINTS and ListAppend.index(
                            PossiblePoint) not in IndexList:  # if possible point in points and the direction not in index list
                        IndexList.append(ListAppend.index(PossiblePoint))  # appending direction to IndexList

                        if pieces[POINTS.index(
                                PossiblePoint)].color is not ChosenPiece.color:  # if pieces are from diffrent colors
                            Point.append(PossiblePoint)  # appending point

            for index in sorted(set(IndexList))[::-1]:

                if ListAppend[index] not in Point:
                    ListAppend.pop(index)  # if point in forbidden direction

            VectorList.append(set(ListAppend))

        return VectorList

    def CheckRemoval(VectorList: list, WeirdList: list):

        for i in range(len(VectorList)):

            for piece in WeirdList:

                if piece.function == PawnVectorWhite:
                    VectorList[i] = list(filter(lambda x: (x != (piece.x + 1, piece.y - 1)
                                                           and x != (piece.x - 1, piece.y - 1)), VectorList[i]))

                if piece.function == PawnVectorBlack:
                    VectorList[i] = list(filter(lambda x: (x != (piece.x + 1, piece.y + 1)
                                                           and x != (piece.x - 1, piece.y + 1)), VectorList[i]))

                else:
                    for Points in action(piece, list(filter(lambda x: x != (King.x, King.y), POINTS))):
                        VectorList[i] = list(filter(lambda x: x not in Points, VectorList[i]))

                    for Points in action(piece, list(filter(lambda x: x not in VectorList[i], POINTS))):
                        VectorList[i] = list(filter(lambda x: x not in Points, VectorList[i]))

        return VectorList

    def PawnPromotion(PromotionList: list):
        """
        pawn promotion to what piece
        :param PromotionList:
        :return: score to add allegiance's team
        """

        if ChosenPiece.color == "White":  # if color = white than buttons need to be higher then chosen piece
            Sign = 1
        elif ChosenPiece.color == "Black":
            Sign = -1  # if color = black than buttons need to be lower than chosen piece

        PieceButtonList = []  # list of buttons of pieces - queen button, bishop button, rook button, knight button
        for i in range(4):
            Button = Buttons(RED, ChosenPiece.x * ScreenWidth / 8, (ChosenPiece.y + Sign * i + Sign) * ScreenHeight / 8,
                             ScreenWidth / 8, ScreenHeight / 8, "Hi", None, None)  # button settings

            PieceButtonList.append(Button)

        NewPieceChosen = False  # a new piece parameter

        while not NewPieceChosen:  # while a new piece isn't chosen

            pygame.display.update()  # updating screen changes

            MouseX, MouseY = pygame.mouse.get_pos()  # mouse position

            # event loop
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

            for i in range(4):  # showing New pieces images
                Screen.blit(PromotionList[i].img,
                            (ChosenPiece.x * ScreenWidth / 8, (ChosenPiece.y + Sign * i + Sign) * ScreenHeight / 8))

            if pygame.mouse.get_pressed()[0]:  # if player pressed mouse
                for Button in PieceButtonList:
                    if Buttons.Hover(Button, MouseX, MouseY):  # if player is in button's parameters
                        NewPieceChosen = True  # ending while loop
                        NewPiece = PromotionList[PieceButtonList.index(Button)]  # setting New piece

        # Chosen piece to promoted piece
        ChosenPiece.function = NewPiece.function
        ChosenPiece.img = NewPiece.img
        ChosenPiece.score = NewPiece.score

        return NewPiece.score

    # Piece Player chose in move
    ChosenPiece = None

    # turn player's color
    TurnColor = "White"

    # fonts
    font = pygame.font.SysFont("Poppins", ScreenWidth // 15)
    font2 = pygame.font.SysFont("ariel", 25)
    font3 = pygame.font.SysFont("Poppins", 14)

    # texts in Main Menu
    # ----------------------------------------------------------------------------------------
    RapidText = font2.render("Rapid - Slow Chess (Minutes)", True, WHITE, False)
    BlitzText = font2.render("Blitz - Fast Chess (Minutes)", True, WHITE, False)
    BulletText = font2.render("Bullet - Very Fast Chess (Seconds)", True, WHITE, False)

    InstructionsColorWheel = font3.render("Row Color - Right Click", True, WHITE, False)
    InstructionsColorWheel2 = font3.render("Col Color - Left Click", True, WHITE, False)

    HelperText = font2.render("Helper", True, WHITE, False)

    Credits = font2.render("Chess - by Liron Kaner", True, WHITE, False)

    # ----------------------------------------------------------------------------------------

    # sounds
    # PieceDropping = pygame.mixer.Sound("Recording (4).m4a")

    cnt = 0  # counter to check events only happend once
    Counter = 0  # counter to measure time
    counter = 0

    ScoreBlack = ScoreWhite = 39  # player's score

    RowColor, ColColor = BLACK, white  # colors of the board

    # Color Wheel
    # ----------------------------------------------------------------------------------------
    # Color Wheel's Center
    CenterCircleX, CenterCircleY = 4 * ScreenWidth // 5, 1.35 * ScreenHeight // 4

    pi = math.pi

    # radius
    R = 150

    # ----------------------------------------------------------------------------------------

    run = True

    while run:

        DrawBoard(RowColor, ColColor)

        # Mouse position
        MouseX, MouseY = pygame.mouse.get_pos()

        # Main Menu
        # ----------------------------------------------------------------------------------------------------------------
        if MainButton.color != BLUE:

            # Color Wheel
            # ----------------------------------------------------------------------------------------------------------------
            pygame.draw.rect(Screen, Greyish,
                             ((CenterCircleX - R // 2 - 5, CenterCircleY - R // 2 - 5),
                              (R + 10, R + 10)))  # drawing square

            Angel = 360 / len(ColorList)
            for i in range(len(ColorList)):
                pygame.draw.arc(Screen, ColorList[i], (CenterCircleX - R // 2, CenterCircleY - R // 2, R, R),
                                pi * Angel / 180, pi * (Angel + 360 / len(ColorList)) / 180, 15)  # drawing circle

                Angel += 360 // len(ColorList)

            if pygame.mouse.get_pressed():

                # distance
                Z = ((((CenterCircleX - MouseX) ** 2) + ((CenterCircleY - MouseY) ** 2)) ** 0.5)

                if R - 90 < Z < R - 75:  # if distance from center not in proximity

                    if MouseX <= CenterCircleX:
                        D = ((((CenterCircleX - MouseX) ** 2) + ((CenterCircleY + R // 2 - MouseY) ** 2)) ** 0.5)

                        x = 160 * math.asin(D / R) / pi + 78  # center angel

                        Pos = len(ColorList) - NumberTransfer(
                            x / (160 / len(ColorList))) + 1  # position of chosen color

                    else:
                        D = ((((CenterCircleX - MouseX) ** 2) + ((CenterCircleY - R // 2 - MouseY) ** 2)) ** 0.5)

                        x = 160 * math.asin(D / R) / pi  # center angel

                        Pos = len(ColorList) - NumberTransfer(
                            x / (160 / len(ColorList))) + 1  # position of chosen color

                    if Pos == len(ColorList):
                        Pos = NumberTransfer(x / (160 / len(ColorList))) - 1
                    if Pos > len(ColorList):
                        Pos = 1

                    if pygame.mouse.get_pressed()[0] and RowColor != ColorList[
                        Pos]:  # if mouse pressed and not same colors
                        ColColor = ColorList[Pos]
                    elif pygame.mouse.get_pressed()[2] and ColColor != ColorList[
                        Pos]:  # if mouse pressed and not same colors
                        RowColor = ColorList[Pos]

            # ----------------------------------------------------------------------------------------------------------------

            # titles in Main Menu

            # -------------------------------------------------------------------
            # space between titles
            Space = 10

            Screen.blit(Credits, (ScreenWidth // 2 - Credits.get_width() // 2, 10))

            Screen.blit(ClockImg,
                        (ScreenWidth * 0.25 // 5 - Space,
                         ScreenHeight * 3.2 // 4.5 - Space - ClockImg.get_height()))
            Screen.blit(RapidText, (
                ScreenWidth * 0.25 // 5 + ClockImg.get_width(),
                ScreenHeight * 3.2 // 4.5 - RapidText.get_height() - Space))

            Screen.blit(BlitzImg,
                        (ScreenWidth * 0.25 // 5 - Space,
                         ScreenHeight * 2.2 // 4.5 - Space - ClockImg.get_height()))
            Screen.blit(BlitzText, (
                ScreenWidth * 0.25 // 5 + ClockImg.get_width(),
                ScreenHeight * 2.2 // 4.5 - BlitzText.get_height() - Space))

            Screen.blit(BulletImg,
                        (ScreenWidth * 0.25 // 5 - Space,
                         ScreenHeight * 1.2 // 4.5 - Space - ClockImg.get_height()))
            Screen.blit(BulletText, (ScreenWidth * 0.25 // 5 + ClockImg.get_width(),
                                     ScreenHeight * 1.2 // 4.5 - BulletText.get_height() - Space))

            Screen.blit(InstructionsColorWheel, (CenterCircleX - InstructionsColorWheel.get_width() // 2,
                                                 CenterCircleY - InstructionsColorWheel.get_height() // 2 - InstructionsColorWheel2.get_height()))

            Screen.blit(InstructionsColorWheel2, (CenterCircleX - InstructionsColorWheel.get_width() // 2,
                                                  CenterCircleY - InstructionsColorWheel.get_height() // 2 + InstructionsColorWheel.get_height()))

            Screen.blit(HelperText, ((HelperButton.x + HelperButton1.x) / 2 - HelperText.get_width() // 4,
                                     HelperButton.y - 15 - HelperText.get_height()))

            # -------------------------------------------------------------------

            # buttons in main menu
            for Button in ButtonList:
                MainMenu(Button, MouseX, MouseY)

                DrawButton(Button)

        # -------------------------------------------------------------------------------------------------------------------------

        # The Game
        else:
            # events which need to occur once
            if cnt == 0:
                TimeWhite = TimeBlack = ButtonType[1].amount * 60  # player's time

                if ButtonType[0].text == "960":  # if game mode is 960
                    Mode960()

                # setting point position in POINTS
                POINTS = []
                for piece in pieces:
                    POINTS.append((piece.x, piece.y))

                cnt += 1

            for piece in pieces:
                if piece is ChosenPiece:
                    Screen.blit(piece.img, (int((MouseX - ScreenWidth / 16)),
                                            int((MouseY - ScreenHeight / 16))))

                else:
                    Screen.blit(piece.img,
                                (piece.x * ScreenWidth / 8 + ScreenWidth / 64,
                                 (piece.y * ScreenHeight / 8 + ScreenHeight / 64)))

            if pygame.mouse.get_pressed()[0]:

                TheBoard_x = int(abs(MouseX) // (ScreenWidth / 8))  # Mouse X in board's coordinates
                TheBoard_y = int(abs(MouseY) // (ScreenHeight / 8))  # Mouse Y in board's coordinates

                if (TheBoard_x,
                    TheBoard_y) in POINTS and ChosenPiece is None:  # if Chosen piece isn't selected and piece in board coordinate

                    if ChosenPiece != pieces[POINTS.index((TheBoard_x, TheBoard_y))]:  # new piece chosen
                        counter = 0

                    ChosenPiece = pieces[POINTS.index((TheBoard_x, TheBoard_y))]  # Chosen piece

                if ChosenPiece is not None and ChosenPiece.color is TurnColor:

                    if ChosenPiece.color == "White":  # circle of doubt
                        color = Yellow
                    else:
                        color = Grey

                    if counter == 0:  # finding chosen piece's possible locations ONLY once and not all the time because it is heavy on computer

                        VectorList = action(ChosenPiece, POINTS)  # list of positions from Chess_Settings

                        # Changing turns
                        if ChosenPiece.color == "White":
                            King = KingWhite

                        else:
                            King = KingBlack

                        WeirdList = list(filter(lambda x: x.color != King.color, pieces))

                        if ChosenPiece != King:

                            SaveList = []

                            for i in range(len(VectorList)):

                                for piece in WeirdList:

                                    Save = VectorList[i]

                                    VectorList[i] = list(
                                        filter(lambda x: not any((King.x, King.y) in y for y in action(piece \
                                                                                                       , list(
                                                map(lambda z: x if (z == (ChosenPiece.x, ChosenPiece.y)) else z,
                                                    POINTS)))) \
                                               , VectorList[i]))  # best brother ever

                                    if Save != VectorList[i]:
                                        SaveList.append(piece)

                                for piece in SaveList:
                                    for List in action(ChosenPiece, POINTS):
                                        if (piece.x, piece.y) in List:
                                            VectorList.append([(piece.x, piece.y)])

                        if ChosenPiece == King:
                            ListAppend = []
                            for i in range(len(VectorList)):
                                if (King.x + 2, King.y) not in ListAppend:
                                    if (King.x + 2, King.y) in VectorList[i]:
                                        ListAppend.append((King.x + 2, King.y))

                                if (King.x - 2, King.y) not in ListAppend:
                                    if (King.x - 2, King.y) in VectorList[i]:
                                        ListAppend.append((King.x - 2, King.y))

                            VectorList = CheckRemoval(VectorList, WeirdList)

                            for piece in WeirdList:
                                for b in action(piece, POINTS):
                                    if (King.x + 2, King.y) in ListAppend:
                                        if (King.x + 1, King.y) in b or (King.x + 2, King.y) in b:
                                            ListAppend.remove((King.x + 2, King.y))
                                    if (King.x - 2, King.y) in ListAppend:
                                        if (King.x - 1, King.y) in b or (King.x - 2, King.y) in b:
                                            ListAppend.remove((King.x - 2, King.y))

                            for a in ListAppend:
                                VectorList.append([a])

                        counter = 1

                    if ButtonType[2].text == "Yes":  # if help was chosen - then show dots
                        for PointList in VectorList:
                            for Point in PointList:
                                pygame.draw.circle(Screen, color, (((Point[0] + 0.5) * (ScreenWidth / 8)),
                                                                   ((Point[1] + 0.5) * ScreenHeight / 8)),
                                                   ScreenWidth / 55)  # Drawing circles

            else:  # if mouse isn't clicked
                if ChosenPiece is not None:  # if piece was chosen
                    if ChosenPiece.color == TurnColor:  # if it is the player's turn

                        for PointList in VectorList:

                            if (TheBoard_x, TheBoard_y) in PointList:  # if chosen place is in list of possible places

                                # if chosen piece went to a populated square
                                if (TheBoard_x, TheBoard_y) in POINTS:

                                    # piece in chosen place (TheBoard_X, TheBoard_Y)
                                    PointChosen = pieces[POINTS.index((TheBoard_x, TheBoard_y))]

                                    # subtracting the other player's score
                                    if PointChosen.color == "White":
                                        ScoreWhite -= PointChosen.score
                                    else:
                                        ScoreBlack -= PointChosen.score

                                    # removing piece in wanted location
                                    POINTS.remove((TheBoard_x, TheBoard_y))
                                    pieces.remove(PointChosen)

                                # changing place in POINTS list
                                POINTS[POINTS.index((ChosenPiece.x, ChosenPiece.y))] = TheBoard_x, TheBoard_y

                                # moving piece to chosen location
                                ChosenPiece.x, ChosenPiece.y = TheBoard_x, TheBoard_y

                                # Castle
                                # ----------------------------------------------------------------
                                if ChosenPiece.function == KingVector:  # if chosen piece is a king
                                    if ChosenPiece.color == "White":
                                        Rook, Rook2 = RookList[0], RookList[1]  # the king's rooks

                                    else:
                                        Rook, Rook2 = RookList[2], RookList[3]

                                    if (ChosenPiece.x, ChosenPiece.y) == (
                                            Rook.x + 2,
                                            Rook.y):  # if chosen place is to castle than change the rook's position

                                        POINTS[POINTS.index((Rook.x, Rook.y))] = (
                                            Rook.x + 3, Rook.y)  # updating rook position in POINTS list
                                        Rook.x += 3  # updating rook position

                                    if (ChosenPiece.x, ChosenPiece.y) == (Rook2.x - 1, Rook2.y):
                                        POINTS[POINTS.index((Rook2.x, Rook2.y))] = (
                                            Rook2.x - 2, Rook2.y)  # updating rook positon in POINTS list
                                        Rook2.x -= 2  # updating

                                # ----------------------------------------------------------------

                                # P.P (Pawn Promotion) - LOL
                                # -------------------------------------------------------------------------

                                if ChosenPiece.function == PawnVectorWhite and ChosenPiece.y == 0:
                                    PromotionList = [QueenWhite, RookWhite, BishopWhite, KnightWhite]
                                    NewScore = PawnPromotion(PromotionList)

                                    # raising score
                                    ScoreWhite = ScoreWhite + NewScore - 1

                                if ChosenPiece.function == PawnVectorBlack and ChosenPiece.y == 7:
                                    PromotionList = [QueenBlack, RookBlack, BishopBlack, KnightBlack]
                                    NewScore = PawnPromotion(PromotionList)

                                    # raising score
                                    ScoreBlack = ScoreBlack + NewScore - 1

                                # -------------------------------------------------------------------------

                                # Changing turns
                                if ChosenPiece.color == "White":
                                    TurnColor = "Black"
                                    King = KingBlack

                                else:
                                    TurnColor = "White"
                                    King = KingWhite

                                # player attribute - self.move (Chess_Settings), if player hasn't moved yet
                                if not ChosenPiece.move:
                                    ChosenPiece.move = True  # piece has moved

                                # sound
                                # if ButtonType[3].text == "Yes":
                                #     pygame.mixer.Sound.play(PieceDropping)

                                # chosen piece has moved, breaking loop
                                break

                # there is no chosen piece to move therefore
                ChosenPiece = None

            # Game blit titles
            # ------------------------------------------------------------------------------------------------------------
            if ScoreWhite - ScoreBlack < 0:
                ScoreWhiteDisplay = 0
                ScoreBlackDisplay = ("+" + str(ScoreBlack - ScoreWhite))

            elif ScoreWhite - ScoreBlack > 0:
                ScoreWhiteDisplay = ("+" + str(ScoreWhite - ScoreBlack))
                ScoreBlackDisplay = 0
            else:
                ScoreWhiteDisplay = 0
                ScoreBlackDisplay = 0

            MinutesWhite = int(TimeWhite // 60)
            SecondsWhite = int(TimeWhite - MinutesWhite * 60)
            if SecondsWhite == 0:
                SecondsWhite = "00"
            elif SecondsWhite < 10:
                SecondsWhite = "0" + str(SecondsWhite)

            MinutesBlack = int(TimeBlack // 60)
            SecondsBlack = int(TimeBlack - MinutesBlack * 60)
            if SecondsBlack == 0:
                SecondsBlack = "00"
            elif SecondsBlack < 10:
                SecondsBlack = "0" + str(SecondsBlack)

            if TurnColor == "White":
                ColorWhite = GREEN
                ColorBlack = WHITE
            else:
                ColorWhite = WHITE
                ColorBlack = GREEN

            WhiteText = font2.render("White", True, ColorWhite, False)
            TimeWhiteText = font2.render(("Time Left = " + str(MinutesWhite) + " : " + str(SecondsWhite)), True, WHITE,
                                         False)
            ScoreWhiteText = font2.render("Score = " + str(ScoreWhiteDisplay), True, WHITE, False)

            BLackText = font2.render("Black", True, ColorBlack, False)
            TimeBlackText = font2.render(("Time Left = " + str(MinutesBlack) + " : " + str(SecondsBlack)), True, WHITE,
                                         False)
            ScoreBlackText = font2.render(" Score = " + str(ScoreBlackDisplay), True, WHITE, False)

            Screen.blit(TimeWhiteText, (0, ScreenHeight // 2 - TimeWhiteText.get_height()))
            Screen.blit(ScoreWhiteText, (0, ScreenHeight // 2 + TimeWhiteText.get_height() // 2))
            Screen.blit(WhiteText, (0, ScreenHeight // 2 - 2.5 * TimeWhiteText.get_height()))

            Screen.blit(BLackText,
                        (ScreenWidth - BLackText.get_width(), ScreenHeight // 2 - 2.5 * TimeWhiteText.get_height()))
            Screen.blit(ScoreBlackText,
                        (ScreenWidth - ScoreBlackText.get_width(), ScreenHeight // 2 + TimeWhiteText.get_height() // 2))
            Screen.blit(TimeBlackText,
                        (ScreenWidth - TimeBlackText.get_width(), ScreenHeight // 2 - TimeWhiteText.get_height()))
            # ------------------------------------------------------------------------------------------------------------

            # Second Passed, update player time
            if Counter == FPS:
                if TurnColor == "White":
                    TimeWhite -= 1
                else:
                    TimeBlack -= 1
                Counter = 0
            Counter += 1

            # if Checkmate
            # ---------------------------------------------
            if KingWhite not in pieces or TimeWhite == 0:
                print("Black has Won")
                run = False

            if KingBlack not in pieces or TimeBlack == 0:
                print("White has Won")
                run = False
            # ---------------------------------------------

        # event loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)

        pygame.display.update()

main()