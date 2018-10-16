# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 20:01:26 2018

@author: heier
"""

from Player import Player
from MinMax import MinMax
from TicTacToe import TicTacToe
from TTTPlayer import TTTPlayer

class TTTMinMax(Player):
    
    def __init__(self, playerID, difficulty):
        self.ID = playerID
        self.diff = difficulty
        self.MM = MinMax(self, self)
    
    def readyPlayer(self):
        pass
    
    def queryAction(self, state):
        print("Beginning MinMax.")
        best = self.MM.MinMaxGo(None, state, self.diff)
        return best[0]
     
    # Heuristic used to evaluate a state.
    def evaluate(self, state):
        result = state.gameover()
        
        if result == -1: # Game not over
            # Count number of possible 3s in a row to get
            score = 0
            
            # Go through rows
            for i in range(0,3):
                ours, theirs, neither = 0, 0, 0
                for j in range(0,3):
                    if state.board[i][j] == 0:
                        ++neither
                    elif state.board[i][j] == self.ID:
                        ++ours
                    else:
                        ++theirs
                # possible results
                score += self.singleScore(ours, theirs, neither)
            
            # Go through columns
            for i in range(0,3):
                ours, theirs, neither = 0, 0, 0
                for j in range(0,3):
                    if state.board[j][i] == 0:
                        ++neither
                    elif state.board[j][i] == self.ID:
                        ++ours
                    else:
                        ++theirs
                # possible results
                score += self.singleScore(ours, theirs, neither)
            
            # Diagonal UL to DR
            for i in range(0,3):
                ours, theirs, neither = 0, 0, 0
                if state.board[i][i] == 0:
                    ++neither
                elif state.board[i][i] == self.ID:
                    ++ours
                else:
                    ++theirs
            # possible results
            score += self.singleScore(ours, theirs, neither)
            
            # Diagonal UR to DL
            for i in range(0,3):
                ours, theirs, neither = 0, 0, 0
                if state.board[i][2-i] == 0:
                    ++neither
                elif state.board[i][2-i] == self.ID:
                    ++ours
                else:
                    ++theirs
            # possible results
            score += self.singleScore(ours, theirs, neither)
            return score
        elif result == 0: # Tie
            return 0
        elif result == self.ID:
            return 500
        else:
            return -500
        
    def singleScore(self, ours, theirs, neither):
        score = 0
        if ours == 1 and neither == 2:
            score+= 1
        elif ours == 2 and neither == 1:
            score += 2
        elif theirs == 1 and neither == 2:
            score -= 1
        elif theirs == 2 and neither ==1:
            score -= 2
        return score

p1 = TTTPlayer(1)
p2 = TTTMinMax(2)

g = TicTacToe(p1, p2)
g.runGame()
        
        
        
        
        
        
        
        
        
        