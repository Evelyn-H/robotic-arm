# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:20:16 2018

@author: heier
"""

from sklearn import svm
import numpy as np
from CategoryLoader import CategoryLoader

class DrawSVM:
    
    def __init__(self):
        self.svm = svm.SVC()
        self.cl = CategoryLoader()
        
    def train(self, cat, n=100):
        print("Initializing SVM training")
        l = list(cat)
        label = np.array(l, dtype=np.float64).reshape(len(l), 1)
        data = cl.load(cat, n, 0, True)
        
        print("Extracting HOG features")
        
        
        
        

dsvm = DrawSVM()
dsvm.train((0,1,2))
