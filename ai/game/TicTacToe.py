# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:26:01 2018

@author: heier

TicTacToe game! Ensures right turn ordering, etc.
"""

class TicTacToe:
    state = None
    p1 = None
    p2 = None
    currentPlayer = None
    Winner = None
    
    def __init__(self, player1, player2):
        global p1, p2, currentPlayer
        p1 = player1
        p2 = player2
        currentPlayer = p1
        
        # TODO: Prepare new game state.
        
        p1.readyPlayer()
        p2.readyPlayer()
    
    def nextTurn(self):
        pass
    