# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:02:08 2018

@author: heier

All the utility/control needed to run Tic Tac Toe
on robot arm.
"""
import sys
sys.path.insert(0, 'C:/Users/heier/Desktop/robotic-arm/main')
from vision import Vision

class TTTRoboAI:
    
    def constructBoard(circles, gridpoints):
        # Sort by x coordinate.
        gridpoints.sort(key=lambda point: point[0])
        print(gridpoints)
        

# Testing
aaa = TTTRoboAI()
vvv = Vision()
circles, gridpoints = vvv.get_gamestate()
aaa.constructBoard(circles, gridpoints)
        