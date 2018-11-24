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
        # Sort by x coordinate.
        gridpoints.sort(key=lambda point: point[0])
        print(gridpoints)
        
        
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
        
        
        

# Testing
aaa = TTTRoboAI()
circles, gridpoints = vvv.get_gamestate()
aaa.constructBoard(circles, gridpoints)
        