# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:22:15 2018

@author: heier
"""

class HOGFinder:
    
    def __init__(self):
        print("Initializing HOGFinder")
    
    # Given a list of 2D uint-8 numpy img arrays
    # it returns the HoG of those images.
    def findHOG(self, imgList):
        print("Finding HOGs")
        