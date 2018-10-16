# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:42:33 2018

@author: heier

TicTacToe state.
"""

from TTTAction import TTTAction
from State import State

class TTTState(State):
    
    # Methods
    def __init__(self, p1, p2):
        self.board = [[0,0,0], [0,0,0], [0,0,0]]
        self.history = []
        self.p1 = p1
        self.p2 = p2
        self.current = self.p1
    
    def __str__(self):
        
        s = "Current Board:\n"
        s += "Player: " + str(self.current.ID) + "\n"
        for i in range(0,3):
            for j in range(0,3):
                s
                s += str(self.board[i][j]) + " "
            s += "\n"
        return s
    
    def actionSpace(self, player):
        actions = []
        for i in range(0,3):
            for j in range(0,3):
                if self.board[i][j] == 0:
                    actions.append(TTTAction(player.ID,i,j))
        
        return actions
    
    def update(self, action):
        self.board[action.x][action.y] = action.played
        self.history.append(action)
        
        if self.current == self.p1:
            self.current = self.p2
        else:
            self.current = self.p1
        
    def reverse(self):
        a = self.history.pop()
        self.board[a.x][a.y] = 0
        if self.current == self.p1:
            self.current = self.p2
        else:
            self.current = self.p1
    
    def threeInRow(self):
        # Rows
        if (self.board[0][0] == self.board[0][1] 
                and self.board[0][1] == self.board[0][2] 
                and self.board[0][0] != 0):
            return self.board[0][0]
        
        if (self.board[1][0] == self.board[1][1] 
                and self.board[1][1] == self.board[1][2] 
                and self.board[1][0] != 0):
            return self.board[1][0]
        
        if (self.board[2][0] == self.board[2][1] 
                and self.board[2][1] == self.board[2][2]
                and self.board[2][0] != 0):
            return self.board[2][0]
        
        # Columns
        if (self.board[0][0] == self.board[1][0] 
                and self.board[1][0] == self.board[2][0]
                and self.board[0][0] != 0):
            return self.board[0][0]
        
        if (self.board[0][1] == self.board[1][1] 
                and self.board[1][1] == self.board[2][1]
                and self.board[0][1] != 0):
            return self.board[0][1]
        
        if (self.board[0][2] == self.board[1][2] 
                and self.board[1][2] == self.board[2][2]
                and self.board[0][2] != 0):
            return self.board[0][2]
        
        # Diagonals
        if (self.board[0][0] == self.board[1][1] 
                and self.board[1][1] == self.board[2][2]
                and self.board[0][0] != 0):
            return self.board[0][0]
        
        if (self.board[0][2] == self.board[1][1] 
                and self.board[1][1] == self.board[2][0]
                and self.board[0][2] != 0):
            return self.board[0][2]
        
        # No threes in a row.
        return None
    
    
    def gameover(self):
        win = self.threeInRow()
        if (win == None and len(self.history) < 9):
            return -1
        elif win != None:
            return win
        else:
            return 0
    
    
            
            
            
            
            
            
            
    