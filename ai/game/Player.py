# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 10:15:56 2018

@author: heier

    Abstract class for any player participating in
    a turn-based type of game.
"""

from abc import ABC, abstractmethod



class Player(ABC):
    playerID = -1 # -1 Means player number is currently unassigned.
    
    # Ready player before game begins.
    @abstractmethod
    def readyPlayer(self):
        pass
    
    # Ask player for their move.
    @abstractmethod
    def queryAction(self, state):
    