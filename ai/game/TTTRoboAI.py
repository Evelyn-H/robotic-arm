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

class TTTRoboAI:
    
    def __init__(self, vision, humanTurn):
        self.game = None
        self.humanTurn = humanTurn
        self.vision = vision
    
    def constructBoard(self, circles, gridpoints):
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
        return board
                    
                    
        
        
    def runGame(self):
        # Set up players and board
        self.game = TTTState(self, self)
        # Robot side
        # Human side
        
        # Who goes first determined by robotFirst
        # Tell them to wait
        # Initiate game loop
        
        # While the game is not over
        while(self.game.gameover() < 0):
        #   if human turn
            if self.humanTurn:
                print("Human turn")
        #       check every 1 (?) sec
        #       if game state changes
        #           Next turn
        #   if robot turn
            else:
                print("Robot turn")
        #       Decide next move
        #       Execute move
        #       When done, signal next turn
        #
        # Game over, signal winner
        
    def determineHumanAction(self):
        # To be finished.
        return
        
        

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
        