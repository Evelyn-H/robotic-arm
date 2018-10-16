# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 09:48:09 2018

@author: heier

    Abstract class for the state of what might be a game.
    Possible actions can be queried from the state.
    The state also contains the logic for advancing
    or reversing its game given actions.
    It should therefore keep a history of played actions
    and relevant information that may need to be saved
    as players make moves.

"""

from abc import ABC, abstractmethod

class State(ABC):
    
    # Given a player, return all the possible actions a player can
    # make given this state. 
    @abstractmethod
    def actionSpace(self, player):
        pass
    
    # Given an action, the state will update itself
    # with the given action.
    @abstractmethod
    def update(self, action):
        pass
    
    # When called, the state will be brought back one action
    # back in time.
    @abstractmethod
    def reverse(self):
        pass
        
    