# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:07:43 2019

@author: heier
"""

import time
from vision import Vision


class DrawGame:
    def __init__(self):
        print("Begginging drawing recognition game!")
        self.v = Vision()
        
    
    def run_game(self, times=3):
        current = 0
        
        # Robot draws bounds.
         self.arm.move_back()
         FormatConvert.drawFromFile(boundFile, self.arm, speed=3)
         self.arm.move_away()
        # Small wait
        time.sleep(1)
        # Do game loop
        while current < times:
            # Human draws
            # Wait until human is "finished"
            input("Press enter when finished...")
            
            # When human is finished, detect category
            img = self.flush_and_get()
            
            # Get drawing of a category
            
            # Robot draws the category
            
            # Tiny wait
            time.sleep(1)
        print("Game over!")
        
    def flush_and_get(self):
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        img = self.v._getImage(self.v.cam1)
        
        return img
        
        