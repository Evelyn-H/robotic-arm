# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 17:11:13 2018

@author: heier
"""
import math

class MinMax:
    
    infinity = 1000 # Assumed to be larger than any value the heuristic
    # might return.
    
    def __init__(self, player, heuristic):
        self.player = player
        self.heuristic = heuristic
    
    # Implementation of depth-limited MinMax
    # Returns most optimal action
    # Note that player using this MinMax is an instance variable.
    # Furthermore, value is returned with its assosciated action.
    def MinMaxGo(self, action, state, depth):
        global infinity
        state.update(action)
        if action != None and (depth == 0 or state.gameover() != -1):
            return (action, self.heuristic.evaluate(state))
        
        if state.current == self.player: # Max
            best = (None, -infinity)
            actions = state.actionSpace(state.current)
            for a in actions:
                option = MinMaxGo(a, state, depth-1)
                state.reverse()
                if best[1] < option[1]:
                    best[1] = option[1]
            return best
        else: # Min
            worst = (None, infinity)
            actions = state.actionSpace(state.current)
            for a in actions:
                option = MinMaxGo(a, state, depth-1)
                state.reverse()
                if worst[1] > option[1]:
                    worst[1] = option[1]
            return worst
                
        