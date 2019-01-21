# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 17:11:13 2018

@author: heier
"""

class MinMax:
    
    def __init__(self, player, heuristic):
        self.player = player
        self.heuristic = heuristic
        # Assumed to be larger than any value the heuristic
        # might return.
        self.infinity = 1000
        
    
    # Implementation of depth-limited MinMax
    # Returns most optimal action
    # Note that player using this MinMax is an instance variable.
    # Furthermore, value is returned with its assosciated action.
    def MinMaxGo(self, action, state, depth):
        print("Entered " + str(depth))
        print("Action: " + str(action))
        print(state)
        global infinity
        if action != None:
            state.update(action)
            print("Updated state:\n", state)
            if (depth == 0 or state.gameover() != -1):
                h = self.heuristic.evaluate(state)
                print("End reached, evaluation: " + str(h))
                input()
                return [action, h]
#        print("Step.")
#        input()
        
        if state.current == self.player: # Max
            print("Max player.")
            best = [None, -self.infinity]
            actions = state.actionSpace(state.current)
            print("Possible actions: \n")
            print(str(list(map(str, actions))))
            input()
            for a in actions:
                option = self.MinMaxGo(a, state, depth-1)
                state.reverse()
                print("Reversed state:\n" + str(state))
                print("Returned: " + str(option[1]))
                print("For action: " + str(a))
                print("Step")
                input()
                print("Best(" + str(best[1]) + ") vs Opt(" + str(option[1]) + ")")
                if best[1] < option[1]:
                    print("Best replaced")
                    best[0] = a
                    best[1] = option[1]
            return best
        else: # Min
            print("Min player.")
            worst = [None, self.infinity]
            actions = state.actionSpace(state.current)
            print("Possible actions: \n")
            print(str(list(map(str, actions))))
            input()
            for a in actions:
                option = self.MinMaxGo(a, state, depth-1)
                state.reverse()
                print("Reversed state:\n" + str(state))
                print("Returned: " + str(option[1]))
                print("For action: " + str(a))
                print("Step")
                input()
                print("Worst(" + str(worst[1]) + ") vs Opt(" + str(option[1]) + ")")
                if worst[1] > option[1]:
                    print("Worst replaced")
                    worst[0] = a
                    worst[1] = option[1]
            return worst
                
        