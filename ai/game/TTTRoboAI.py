# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:02:08 2018

@author: heier

All the utility/control needed to run Tic Tac Toe
on robot arm.
"""
import sys
sys.path.insert(0, 'C:/Users/heier/Desktop/robotic-arm/main')
import TestGridCircles

class TTTRoboAI:
    
    def __init__(self, robotFirst):
        self.game = TicTacToe(self, self)
    
    def constructBoard(self, circles, gridpoints):
        # Gridpoints should be only the gridpoints of the board
        # Unecessary points from noise should not be present.
        # Sort by x coordinate.
        gridpoints.sort(key=lambda point: point[0])
        
        
    def runGame(self):
        # Set up players and board
        # Robot side
        # Human side
        
        # Decide who goes first
        # Tell them to wait
        # Initiate game loop
        
        # While the game is not over
        #   if human turn
        #       and game state changes
        #           Next turn
        #   if robot turn
        #       Decide next move
        #       Execute move
        #       When done, signal next turn
        #
        # Game over, signal winner
        
    def determineHumanAction(self):
        # To be finished.
        
        

# Testing
aaa = TTTRoboAI()
circles = 
aaa.constructBoard(circles, gridpoints)
        