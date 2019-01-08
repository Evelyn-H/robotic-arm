# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:02:08 2018

@author: heier

All the utility/control needed to run Tic Tac Toe
on robot arm.
"""
import sys
import cv2
import FormatConvert
sys.path.insert(0, 'C:/Users/heier/Desktop/robotic-arm/main')
sys.path.insert(0, "C:/User/heier/Desktop/robotic-arm/vision/images/top")
from TestGridCircles import TestGridCircles
from ai.game.TTTState import TTTState
from ai.game.TTTAction import TTTAction
from ai.game.TTTMinMax import TTTMinMax

class TTTRoboAI:
    
    def __init__(self, arm, vision, humanTurn):
        self.arm = arm
        # The Game State
        self.game = TTTState(self, self)
        # Who starts?
        self.humanTurn = humanTurn
        # Human ID
        self.hID = 1
        # Robot ID
        self.rID = 2
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
        corners = None
        
    
    
    def constructBoard(self, circles, crosses):    
        print("Circles")
        print(circles)
        
        board = [[0,0,0], [0,0,0], [0,0,0]]
        
        if circles != None:
            for c in circles[0]:
                if c[0] < self.corners[0][0][0]: # Left
                    if c[1] < self.corners[0][0][1]:   # Upper
                        board[0][0] = '1'
                    elif c[1] < self.corners[1][0][1]: # Middle
                        board[1][0] = '1'
                    else:                       # Lower
                        board[2][0] = '1'
                
                elif c[0] < self.corners[0][1][0]: # Middle
                    if c[1] < self.corners[0][0][1]:   # Upper
                        board[0][1] = '1'
                    elif c[1] < self.corners[1][0][1]: # Middle
                        board[1][1] = '1'
                    else:                       # Lower
                        board[2][1] = '1'
                
                else:
                    if c[1] < self.corners[0][0][1]:   # Upper
                        board[0][2] = '1'
                    elif c[1] < self.corners[1][0][1]: # Middle
                        board[1][2] = '1'
                    else:                       # Lower
                        board[2][2] = '1'
            # End assignment of circle positions
        if crosses != None:
            # Assign cross positions
            for x in crosses[0]:
                if x[0] < self.corners[0][0][0]: # Left
                    if x[1] < self.corners[0][0][1]:   # Upper
                        board[0][0] = '2'
                    elif x[1] < self.corners[1][0][1]: # Middle
                        board[1][0] = '2'
                    else:                       # Lower
                        board[2][0] = '2'
                
                elif x[0] < self.corners[0][1][0]: # Middle
                    if x[1] < self.corners[0][0][1]:   # Upper
                        board[0][1] = '2'
                    elif x[1] < self.corners[1][0][1]: # Middle
                        board[1][1] = '2'
                    else:                       # Lower
                        board[2][1] = '2'
                
                else:
                    if x[1] < self.corners[0][0][1]:   # Upper
                        board[0][2] = '2'
                    elif x[1] < self.corners[1][0][1]: # Middle
                        board[1][2] = '2'
                    else:                       # Lower
                        board[2][2] = '2'
            # End assignment of cross positions
        return board
    
    
    # Returns the first difference in a board that is found.
    def firstNewFilledIn(self, new):
        for i in range(0,3):
            for j in range(0,3):
                if self.TTTState.board[i][j]==0 and new[i][j]!=0:
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
            FormatConvert.drawFromFile(gridFile, self.arm)
            # Robot Prep
            # TODO: finish below.
            grid = self.vision.getgridpoints()
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
            
            # Human Prep
            
            # Who goes first determined by robotFirst
            # Tell them to wait
            # Initiate game loop
            self.setup = False
        
        \else: # Setup over, game is running.
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
                    circles = self.vision.getcircles()
                    crosses = self.vision.getcrosses()
                    newBoard = self.constructBoard(circles, crosses)
                    # if game state changes
                    try:
                        x, y = self.firstNewFilledIn(newBoard)
                    except:
                        print("No observed change in state")
                    else:
                        print("New move: ", x, ", ", y) 
                        humanAction = TTTAction(self.hID, x, y)
                        self.game.update(humanAction)
                        # Next turn
                        self.humanTurn = False
                        # if robot turn
                else:
                    print("Robot turn")
                    robotAction = self.minmax.queryAction(self.game.board)
                    self.game.update(robotAction)
                    # Execute move
                    FormatConvert.drawFromFile(crossFile, self.arm,
                                               shift1=(self.drawShift[robotAction.x][robotAction.y][0],
                                                       self.drawShift[robotAction.x][robotAction.y][1]))
                    # When done, signal next turn
                    self.humanTurn = True
            # Game over, signal winner
            else:
                print("Game over! Result: ", self.game.gameover() )
        
    
gridFile="C:/Users/heier/Desktop/robotic-arm/ai/game/TTTLines.txt"
circleFile="C:/Users/heier/Desktop/robotic-arm/ai/game/TTTCircle.txt"
crossFile="C:/Users/heier/Desktop/robotic-arm/ai/game/TTTCross.txt" 


# Testing purposes
#imgStart = cv2.imread('C:/Users/heier/Desktop/robotic-arm/vision/images/top/TTT_001.jpg')
#
#cv2.imshow('image',imgStart)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#
#img2 = imgStart.copy()
#ttt = TestGridCircles()
#gridpoints = ttt._getGridPoints(img2);    
#aaa = TTTRoboAI(ttt, True)
#circles = ttt._detectCircles(img2);
#bbb = aaa.constructBoard(circles, gridpoints)
#print(bbb)
        