# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:02:08 2018

@author: heier

All the utility/control needed to run Tic Tac Toe
on robot arm.
"""
import sys
import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
from ai import FormatConvert
sys.path.insert(0, "ai")
sys.path.insert(0, "vision")
sys.path.insert(0, "ai/game")
sys.path.insert(0, "vision/old/images/top")
from TTTState import TTTState
from TTTAction import TTTAction
from TTTMinMax import TTTMinMax
from vision import Vision
from control.arm import Arm


class TTTRoboAI:

    def __init__(self, arm, vision, humanTurn=False):
        self.arm = arm
        # The Game State
        self.game = TTTState(self, self)

        # Who starts?
        self.humanTurn = humanTurn
        # Human ID
        self.hID = 1
        # Robot ID
        self.rID = 2
        self.ID = self.rID
        # Reference to vision component
        self.vision = vision

        # Current count of blank papers detected
        self.paperBlankCount = 0
        # Threshhold to trigger continuation
        self.paperBlankThresh = 2

        # Setup is happening
        self.setup = True
        # Paper is currently blank
        self.paperBlank = False

        # Robot minmax method.
        self.minmax = TTTMinMax(self.rID, 1)

        # Assumed distance to shift where to draw things
        self.drawShift = [[(-5,-5), (0,-5), (5,-5)],
                           [(-5,0), (0,0), (5,0)],
                           [(-5,5), (0,5), (5,5)]]

        # Grid line intersections
        self.corners = []

        # Cross detection boundary
        self.cross_bound = [[], [], []]

    # Finds the corners in an empty tick tack toe grid.
    def findCorners(self, grid):
        print("Finding corners of grid.")
        self.corners.append(grid[0])
        self.corners.append(grid[1])
        self.corners.append(grid[2])
        self.corners.append(grid[3])
        # sort corners.
        print("Initial corners detected: ", self.corners)
        self.corners.sort(key=lambda point: point[1])
        head = self.corners[0:2]
        head.sort(key=lambda point: point[0])
        tail = self.corners[2:4]
        tail.sort(key=lambda point: point[0])
        self.corners = [head, tail]
        print("Corners sorted: ", self.corners)


    # Cross bounds given as (x1,y1, x2, y2)
    # where the the two xy's are the upper left
    # and lower right corner of a square, respectively.
    def compute_cross_bounds(self, border=10):
        # TODO: double check if width and height is calculated correctly.
        width = (self.corners[0][1][0] - self.corners[0][0][0])-2*border
        height = (self.corners[1][0][1] - self.corners[0][0][1])-2*border

        # Append appropriate bounds
        # Upper row
        self.cross_bound[0].append( (self.corners[0][0][0]-width-border,
                        self.corners[0][0][1]-height-border,
                        self.corners[0][0][0]-border,
                        self.corners[0][0][1]-border))
        self.cross_bound[0].append( (self.corners[0][1][0]-width-border,
                        self.corners[0][1][1]-height-border,
                        self.corners[0][1][0]-border,
                        self.corners[0][1][1]-border))
        self.cross_bound[0].append( (self.corners[0][1][0]+border,
                        self.corners[0][1][1]-height-border,
                        self.corners[0][1][0]+width+border,
                        self.corners[0][1][1]-border))
        # Middle row
        self.cross_bound[1].append( (self.corners[1][0][0]-width-border,
                        self.corners[1][0][1]-height-border,
                        self.corners[1][0][0]-border,
                        self.corners[1][0][1]-border))
        self.cross_bound[1].append( (self.corners[1][1][0]-width-border,
                        self.corners[1][1][1]-height-border,
                        self.corners[1][1][0]-border,
                        self.corners[1][1][1]-border))
        self.cross_bound[1].append( (self.corners[1][1][0]+border,
                        self.corners[1][1][1]-height-border,
                        self.corners[1][1][0]+width+border,
                        self.corners[1][1][1]-border))
        # Lower row
        self.cross_bound[2].append( (self.corners[1][0][0]-width-border,
                        self.corners[1][0][1]+border,
                        self.corners[1][0][0]-border,
                        self.corners[1][0][1]+height+border))
        self.cross_bound[2].append( (self.corners[1][1][0]-width-border,
                        self.corners[1][1][1]+border,
                        self.corners[1][1][0]-border,
                        self.corners[1][1][1]+height+border))
        self.cross_bound[2].append( (self.corners[1][1][0]+border,
                        self.corners[1][1][1]+border,
                        self.corners[1][1][0]+width+border,
                        self.corners[1][1][1]+height+border))

        print("Final bounds: ")
        print(self.cross_bound)

    def filterCrosses(self, crosses):
        # Assign cross positions
        # First, filter out all crosses that are not within bounds.
        print("Filtering crosses (", len(crosses), ")")
        i = 0;
        while i < len(crosses):
            bounded = False
            # If a single boundary contains it, make it true.
            for x in range(3):
                for y in range(3):
                    if (crosses[i][0] >= self.cross_bound[x][y][0]
                        and crosses[i][0] >= self.cross_bound[x][y][1]
                        and crosses[i][1] <= self.cross_bound[x][y][2]
                        and crosses[i][1] <= self.cross_bound[x][y][3]):
                            bounded = True
            if bounded:
                # Go to next
                i += 1
            else:
                # Remove
                crosses.pop(i)
            # End while.
        print("Crosses left: ", len(crosses))
        return crosses

    def constructBoard(self, circles, crosses):
        crosses = crosses.tolist() # Convert to regular list
#        print("Circles")
#        print(circles)
#        print("Crosses (unfiltered)")
#        print(crosses)

        if circles is None:
            print("No circles!")
            circles = [[]]
        if crosses is None:
            print("No (unfiltered) crosses!")
            crosses = [[]]

        board = [[0,0,0], [0,0,0], [0,0,0]]
        print("Adding circles to board")
        for c in circles[0]:
            if c[0] < self.corners[0][0][0]: # Left
                if c[1] < self.corners[0][0][1]:   # Upper
                    if board[0][0]==0:
                        board[0][0] = 1
                elif c[1] < self.corners[1][0][1]: # Middle
                    if board[1][0]==0:
                        board[1][0] = 1
                elif board[2][0]==0:               # Lower
                    board[2][0] = 1

            elif c[0] < self.corners[0][1][0]: # Middle
                if c[1] < self.corners[0][0][1]:   # Upper
                    if board[0][1]==0:
                        board[0][1] = 1
                elif c[1] < self.corners[1][0][1]: # Middle
                    if board[1][1]==0:
                        board[1][1] = 1
                elif board[2][1]==0:               # Lower
                    board[2][1] = 1

            else:
                if c[1] < self.corners[0][0][1]:   # Upper
                    if board[0][2]==0:
                        board[0][2] = 1
                elif c[1] < self.corners[1][0][1]: # Middle
                    if board[1][2]==0:
                        board[1][2] = 1
                elif board[2][2]==0:                      # Lower
                    board[2][2] = 1
        # End assignment of circle positions

        crosses = self.filterCrosses(crosses)
#        print("Board so far: ")
#        print(board)
#        print("Corners: ")
#        print(self.corners[0][0], ' ', self.corners[0][1])
#        print(self.corners[1][0], ' ', self.corners[1][1])
#        print("Adding crosses to board")
        # Add crosses in appropriate places where there are no circles.
        for x in crosses:
            print(x)
#            ic = img.copy()

            if x[0] < self.corners[0][0][0]: # Left
                if x[1] < self.corners[0][0][1]:
                    if board[0][0]==0:   # Upper
                        board[0][0] = 2
#                        print('leftup')
                elif x[1] < self.corners[1][0][1]:
                    if board[1][0]==0: # Middle
                        board[1][0] = 2
#                        print('leftmid')
                elif board[2][0]==0:                       # Lower
                    board[2][0] = 2
#                    print('leftlow')
#                else:
#                    print("left...")

            elif x[0] < self.corners[0][1][0]: # Middle
                if x[1] < self.corners[0][0][1]:
                    if board[0][1]==0:   # Upper
                        board[0][1] = 2
#                        print('midup')
                elif x[1] < self.corners[1][0][1]:
                    if board[1][1]==0: # Middle
                        board[1][1] = 2
#                        print('midmid')
                elif board[2][1]==0: # Lower
                    board[2][1] = 2
#                    print('midlow')
#                else:
#                    print("mid...")

            else:
                if x[1] < self.corners[0][0][1]:
                    if board[0][2]==0:   # Upper
                        board[0][2] = 2
#                        print('rightup')
                elif x[1] < self.corners[1][0][1]:
                    if board[1][2]==0: # Middle
                        board[1][2] = 2
#                        print('rightmid')
                elif board[2][2]==0: # Lower
                    board[2][2] = 2
#                    print('rightlow')
#                else:
#                    print('right...')

#            cv2.rectangle(ic, (x[0], x[1]), (x[0]+1,x[1]+1), (0,255,0), 2)
#            cv2.imshow('image',ic)
#            cv2.waitKey(0)
#            cv2.destroyAllWindows()
            # End assignment of cross positions
        return board


    # Returns the first difference in a board that is found.
    def firstNewFilledIn(self, new):
        for i in range(0,3):
            for j in range(0,3):
                if self.game.board[i][j]==0 and new[i][j] == self.hID:
                    return i, j
        # Boards are completely similar in this case
        return None


    # The game needs to run without taking breaks, in other words
    # It will be a method where the AI calls it multiple times when it feels
    # like it, because we do not want this to slow down any other parts.
    def gameTick(self):
        # Setup
        if self.setup:
            print("Setup")
            # Assume board starts out blank.
            print("Drawing board")
            # Draw grid, save what the location should be
            # FormatConvert.drawFromFile(gridFile, self.arm, speed=4)
            self.arm.move_away()

            print("Waiting a bit")
            time.sleep(1)
            print("Done waiting")

            # Robot Prep
            # Find corners.
            self.findCorners(self.vision.get_gamegrid())
            # Now define the square bounds needed for adding crosses.
            self.compute_cross_bounds()

            # Human Prep (Not necessary)

            # Who goes first determined by robotFirst
            # Initiate game loop
            self.setup = False

        else: # Setup over, game is running.
            print("Game loop")
            # While the game is not over
            if self.game.gameover() == -1:
                # if human turn
                # Note: Maybe want to put the entire thing for sides
                # deciding which action to take in a separate method, for more
                # readability?
                if self.humanTurn:
                    print("Human turn")
                    # Note: either there must be something catching
                    # get_gamestate() in case it finds no solution
                    # and logically returns null...
                    # Either that, or we must never allow it to fail.
                    # TODO: GET RIGHT METHODS BELOW.
                    circles, crosses = self.vision.get_gamestate(self.cross_bound)
                    newBoard = self.constructBoard(circles, crosses)
                    print('new', newBoard)
                    # if game state changes
                    try:
                        x, y = self.firstNewFilledIn(newBoard)
                    except Exception as e:
                        print("No observed change in state")
                        print(e)
                    else:
                        print("New move: ", x, ", ", y)
                        humanAction = TTTAction(self.hID, x, y)
                        self.game.update(humanAction)
                        # Next turn
                        self.humanTurn = False
                        # if robot turn
                    print('state', self.game, '\n cx', circles, crosses)
                else:
                    print("Robot turn")
                    robotAction = self.minmax.queryAction(self.game)
                    print('r', self.game.board)
                    self.game.update(robotAction)
                    print('r', self.game.board)
                    # Execute move
                    self.arm.move_back()
                    FormatConvert.drawFromFile(crossFile, self.arm,
                                               shift1=(self.drawShift[robotAction.x][robotAction.y][0],
                                                       self.drawShift[robotAction.x][robotAction.y][1]), speed=4)
                    self.arm.move_away()
                    # When done, signal next turn
                    self.humanTurn = True
            # Game over, signal winner
            else:
                print("Game over! Result: ", self.game.gameover() )

    def drawCrossBounds(self, img):
        for row in range(3):
            for col in range(3):
                n = 3*row + col
                cv2.rectangle(img, (self.cross_bound[row][col][0],
                                    self.cross_bound[row][col][1]),
                        (self.cross_bound[row][col][2],
                         self.cross_bound[row][col][3]),
                         (0,n*(255/9),0), 3 )

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def game_loop(self):
        last_time = time.time()
        while self.game.gameover() == -1:
            now_time = time.time()
            if (not self.vision.is_hand_in_the_way() and now_time - last_time > 1):
                self.gameTick()
                last_time = time.time()

        print("Game Done.")


if __name__ == '__main__':

    gridFile = "ai/game/TTTLines.txt"
    circleFile = "ai/game/TTTCircle.txt"
    crossFile = "ai/game/TTTCross.txt"

    try:
        arm = Arm('/dev/ttyACM0')
    except Exception as e:
        arm = Arm('/dev/ttyACM1')

    v = Vision()

    # for i in range(100):
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     img = v.get_image_top_camera()
    #     # _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
    #     # img = np.rot90(img, 3)
    #     # img = img[630:810, 260:440]
    #     name = "TTT" + "_" + str(i) + ".png"
    #     cv2.imwrite(name, img)
    #     cv2.imshow('frame', img)
    #     while not cv2.waitKey(1) & 0xFF == ord('c'):
    #         pass

    t = TTTRoboAI(arm, v, False)
    t.game_loop()


    #
    # # Testing purposes
    # i2 = cv2.imread('vision/old/images/top/TTT_004.jpg')
    # cv2.imshow('image',i2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # g2 = cv2.cvtColor(i2, cv2.COLOR_BGR2GRAY)
    #
    # #b2 = cv2.GaussianBlur(g2,(5,5),0)
    # b2 = cv2.medianBlur(g2, 5)
    # cv2.imshow('image',b2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # _, tb2 = cv2.threshold(b2, 127, 255, cv2.THRESH_BINARY_INV)
    #
    # #sx = cv2.Sobel(tb2,cv2.CV_64F,1,0,ksize=5)
    # #sy = cv2.Sobel(tb2,cv2.CV_64F,0,1,ksize=5)
    # #
    # #cv2.imshow('image',sx)
    # #cv2.waitKey(0)
    # #cv2.destroyAllWindows()
    # #cv2.imshow('image',sy)
    # #cv2.waitKey(0)
    # #cv2.destroyAllWindows()
    #
    # g2c = g2.copy()
    #
    # v = Vision()
    # t = TTTRoboAI(None, v, None)
    # grid = v._getGridPoints(i2)
    # print("Grid: \n", grid)
    # t.findCorners(grid)
    # print("Corners: \n", t.corners)
    # t.compute_cross_bounds()
    # print("Bounds: \n", t.cross_bound)
    #
    #
    # circles = v._detectCircles(i2)
    # crosses = v._detectCorners(i2)
    #
    # c_filter = t.filterCrosses(crosses.tolist())
    #
    # for x in c_filter:
    #     cv2.rectangle(g2c, (x[0], x[1]), (x[0]+1,x[1]+1), (0,255,0), 1)
    #
    # cv2.imshow('image',g2c)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #
    # board = t.constructBoard(circles, crosses, i2.copy())
    #
    # print("Board: \n", board)
