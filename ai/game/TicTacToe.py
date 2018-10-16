# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:26:01 2018

@author: heier

TicTacToe game! Ensures right turn ordering, etc.
"""

from TTTState import TTTState
from TTTPlayer import TTTPlayer

class TicTacToe:
    
    def __init__(self, player1, player2):
        self.state = TTTState()
        self.p1 = player1
        self.p2 = player2
        self.currentPlayer = self.p1
        self.winner = None
        
        # These end when player signals they are ready to 
        # begin the game.
        self.p1.readyPlayer()
        self.p2.readyPlayer()
    
    def nextTurn(self):
        self.state.update(self.currentPlayer.queryAction(self.state))
        if (self.currentPlayer == self.p1):
            self.currentPlayer = self.p2
        else:
            self.currentPlayer = self.p1
                
    def runGame(self):
        print("TicTacToe game begun.\n")
        print(self.state)
        while(self.state.gameover() == -1):
            self.nextTurn()
            print(self.state)
            print("\n")
        
        # Game is finished!
        result = self.state.gameover()
        if (result == 0):
            print("Ah! A tie.")
        elif(result == 1):
            print("Player 1 wins!")
        elif(result == 2):
            print("Player 2 wins!")
        else:
            print("Error.")

p1 = TTTPlayer(1)
p2 = TTTPlayer(2)

g = TicTacToe(p1, p2)
g.runGame()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            