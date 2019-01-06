# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 12:22:15 2018

@author: heier
"""

from skimage.feature import hog
from matplotlib import pyplot as plt
from CategoryLoader import CategoryLoader
import numpy as np

class HOGFinder:
    
    def __init__(self):
        self.ppc = 4 # Pixels per cell
        self.cpb = 2 # Cells per block
    
    # Given a list of 2D uint-8 numpy img arrays
    # it returns the HoG of those images.
    # Currently returns images, later add option
    # to not give images.
    def findHOG(self, imgList, visual):
        hog_img = []
        hog_ftr = []
        for i in range(len(imgList)):
            if visual:
                hf, hi = hog(imgList[i], 
                             pixels_per_cell=(self.ppc, self.ppc),
                             cells_per_block=(self.cpb,self.cpb), 
                             block_norm="L2-Hys",
                             visualise=True)
            else:
                hf = hog(imgList[i], 
                         pixels_per_cell=(self.ppc, self.ppc),
                         cells_per_block=(self.cpb,self.cpb), 
                         block_norm="L2-Hys")
                
            
            hog_ftr.append(hf)
            
            if visual:
                hog_img.append(hi)
            # End for loop
        
        if visual:
            return hog_ftr, hog_img
        else:
            return hog_ftr
    
    def testHOG():
        # Test script
        hogf = HOGFinder()
        cl = CategoryLoader()
        data = cl.loadSingle(0, 10, 1, False)
        features, images = hogf.findHOG(data, True)
                
        w=6
        h=15
        fig=plt.figure(figsize=(w, h))
        rows = 5
        columns = 2
        for i in range(1, rows +1):
            fig.add_subplot(rows, columns, (2*i)-1)
            plt.imshow(data[i-1])
            fig.add_subplot(rows, columns, (2*i))
            plt.imshow(images[i-1])
        plt.show()
        
# HOGFinder.testHOG()