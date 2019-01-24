# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 14:07:43 2019

@author: heier
"""

import sys
import time
from vision import Vision
from ai.FormatConvert import FormatConvert, gridFile, crossFile
from keras.models import load_model
import cv2
import numpy as np
from matplotlib import pyplot as plt



if len(sys.argv) > 1 and sys.argv[1] == 'test':
    from DrawClass import DrawTest
    dt = DrawTest(None)
    dt.testNN()


class DrawGame:
    def __init__(self):
        print("Begginging drawing recognition game!")
        self.v = Vision()
        self.model = load_model("nn_hog.h5")
        self.categories = (
                'airplane',
                'backpack',
                'cactus',
                'dog',
                'ear',
                'face',
                'garden',
                'hamburger',
                'icecream',
                'jacket'
                )

    def run_game(self, times=3):
        current = 0

        # Robot draws bounds.
        self.arm.move_back()
        FormatConvert.drawFromFile("bounds.txt", self.arm, speed=3)
        self.arm.move_away()
        # Small wait
        time.sleep(1)
        # Do game loop
        while current < times:
            # Human draws
            # Wait until human is "finished"
            input("Press enter when finished...")

            # When human is finished, detect category
            img = self.v._getImage(self.v.cam1)
            img_to_predict = self.preprocessing(img)
            
            # Get drawing of a category

            # Robot draws the category

            # Tiny wait
            time.sleep(1)
        print("Game over!")
        
    
    def preprocessing(self, img):
        print("Preprocessing img")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
        img = np.rot90(img, 3)
        img = img[630:810, 260:440]
        plt.imshow(img)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    