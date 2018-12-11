# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:02:08 2018

@author: heier

All the utility/control needed to run Tic Tac Toe
on robot arm.
"""
import sys
import cv2
sys.path.insert(0, 'C:/Users/heier/Desktop/robotic-arm/main')
sys.path.insert(0, "C:/User/heier/Desktop/robotic-arm/vision/images/top")
from TestGridCircles import TestGridCircles
from TTTState import TTTState
from TTTAction import TTTAction
from TTTMinMax import TTTMinMax

class TTTRoboAI:
    
    def __init__(self, vision, humanTurn):
        self.game = TTTState(self, self) # Game
        self.humanTurn = humanTurn # Whose turn is it
        self.hID = 1 # Human id
        self.rID = 2 # Robot id
        self.vision = vision
        
        self.paperBlankCount = 0 # Current count of blank papers detected
        self.paperBlankThresh = 2 # Threshhold to trigger continuation
        
        self.setup = True # Setup is happening
        self.paperBlank = False # Paper is currently blank
        
        self.minmax = TTTMinMax(self.rID, 1) # Robot minmax method.
    
    def constructBoard(self, circles, crosses, gridpoints):
        # Gridpoints should be only the gridpoints of the board
        # Unecessary points from noise should not be present.
        # Sort by x coordinate.
        print(gridpoints)
        gridpoints.sort(key=lambda point: point[1])
        print(gridpoints)
        
        head = gridpoints[0:2]
        head.sort(key=lambda point: point[0])
        tail = gridpoints[2:4]
        tail.sort(key=lambda point: point[0])
        corners = [head, tail]
        print(corners)
        
        print("Circles")
        print(circles)
        
        board = [[0,0,0], [0,0,0], [0,0,0]]
        
        if circles != None:
            for c in circles[0]:
                if c[0] < corners[0][0][0]: # Left
                    if c[1] < corners[0][0][1]:   # Upper
                        board[0][0] = '1'
                    elif c[1] < corners[1][0][1]: # Middle
                        board[1][0] = '1'
                    else:                       # Lower
                        board[2][0] = '1'
                
                elif c[0] < corners[0][1][0]: # Middle
                    if c[1] < corners[0][0][1]:   # Upper
                        board[0][1] = '1'
                    elif c[1] < corners[1][0][1]: # Middle
                        board[1][1] = '1'
                    else:                       # Lower
                        board[2][1] = '1'
                
                else:
                    if c[1] < corners[0][0][1]:   # Upper
                        board[0][2] = '1'
                    elif c[1] < corners[1][0][1]: # Middle
                        board[1][2] = '1'
                    else:                       # Lower
                        board[2][2] = '1'
            # End assignment of circle positions
        if crosses != None:
            # Assign cross positions
            for x in crosses[0]:
                if x[0] < corners[0][0][0]: # Left
                    if x[1] < corners[0][0][1]:   # Upper
                        board[0][0] = '2'
                    elif x[1] < corners[1][0][1]: # Middle
                        board[1][0] = '2'
                    else:                       # Lower
                        board[2][0] = '2'
                
                elif x[0] < corners[0][1][0]: # Middle
                    if x[1] < corners[0][0][1]:   # Upper
                        board[0][1] = '2'
                    elif x[1] < corners[1][0][1]: # Middle
                        board[1][1] = '2'
                    else:                       # Lower
                        board[2][1] = '2'
                
                else:
                    if x[1] < corners[0][0][1]:   # Upper
                        board[0][2] = '2'
                    elif x[1] < corners[1][0][1]: # Middle
                        board[1][2] = '2'
                    else:                       # Lower
                        board[2][2] = '2'
            # End assignment of cross positions
        return board
                  
    # Returns the first difference in a board that is found.
    def firstBoardDifference(self, b1, b2):
        for i in range(0,3):
            for j in range(0,3):
                if b1[i][j] != b2[i][j]:
                    return i, j
        # Boards are completely similar
        return None
                    
    # The game needs to run without taking breaks, in other words
    # It will be a method where the AI calls it multiple times when it feels
    # like it, because we do not want this to slow down any other parts.
    def gameTick(self):
        # Setup
        if self.setup:
            print("Setup")
            # Count how many times a paper is registered
            # as blank before aknowleding it is in fact blank.
            if not self.paperBlank:
                print("Is paper blank?")
                if self.paperBlankCount < self.paperBlankThresh:
                    if self.vision.isPaperEmpty():
                        self.paperBlankCount += 1
                    else:
                        self.paperBlankCount = 0
                else:
                    self.paperBlank = True
            else:
                print("Initializing game")
                # Draw grid, save what the location should be
                # Robot Prep
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
                    circles, gridpoints = self.vision.get_gamestate()
                    newBoard = self.constructBoard(circles, gridpoints)
                    # if game state changes
                    try:
                        x, y = self.firstBoardDifference(newBoard, TTTState.board)
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
                    # When done, signal next turn
                    self.humanTurn = True
            # Game over, signal winner
            else:
                print("Game over! Result: ", self.game.gameover() )
        
    

# Testing purposes
imgStart = cv2.imread('C:/Users/heier/Desktop/robotic-arm/vision/images/top/TTT_001.jpg')

cv2.imshow('image',imgStart)
cv2.waitKey(0)
cv2.destroyAllWindows()

img2 = imgStart.copy()
ttt = TestGridCircles()
gridpoints = ttt._getGridPoints(img2);    
aaa = TTTRoboAI(ttt, True)
circles = ttt._detectCircles(img2);
bbb = aaa.constructBoard(circles, gridpoints)
print(bbb)
        