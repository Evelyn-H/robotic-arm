# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:48:25 2018

@author: heier
"""

from ImgComp import ImgComp
import cv2
import numpy

# Simple comparison method.
class SimpleComp(ImgComp):
    
    def __init__(self, blurIter):
        self.blurIter = blurIter
    
    # Compares two grayscale images
    # Img 2 is the image that gets blurred
    # Consider: Do we standardize images to some
    #           specific format, or do we treat them
    #           once they are received?
    def compare(self, img1, img2):
        
        blurred = img2.copy()
        for i in range(0, self.blurIter):
            # Blur img with gaussian blur
            blurred = cv2.GaussianBlur(blurred, (7,7), 0)
            # True outline must remain clear
            blurred = numpy.add(img2, blurred) 
        
        # Now for comparison.
        # The closer each corrresponding pixel is to each other, the better.
        # Be as close to 0 as possible.
        
        