# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 20:40:17 2018

@author: heier
"""

from TTTPlayer import TTTPlayer
from TTTMinMax import TTTMinMax
from TicTacToe import TicTacToe

p1 = TTTPlayer(1)
p2 = TTTMinMax(2, 1)
g = TicTacToe(p1, p2)
g.runGame()