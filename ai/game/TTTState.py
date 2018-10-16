# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:42:33 2018

@author: heier

TicTacToe state.
"""

import State

class TTTState(State):
    
    board = None
    
    def __init__(self):
        global board
        board = [[0,0,0], [0,0,0], [0,0,0]]
    