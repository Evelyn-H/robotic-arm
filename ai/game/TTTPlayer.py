# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 16:30:07 2018

@author: heier
"""

from Player import Player

class TTTPlayer(Player):
    
    def __init__(self, playerID):
        self.ID = playerID
    
    def readyPlayer(self):
        pass
    
    def queryAction(self, state):
        actions = state.actionSpace(self)
        legalAction = False
        choice = None
        while not legalAction:
            print("Player " + str(self.ID) + " command: ")
            xinp,yinp = input().split()
            x, y = int(xinp), int(yinp)
            # Check if action is possible.
            for i in range(0, len(actions)):
                if actions[i].x == x and actions[i].y == y:
                    legalAction = True
                    choice = actions[i]
        
        return choice
            
        