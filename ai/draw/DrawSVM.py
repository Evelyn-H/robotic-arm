# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:20:16 2018

@author: heier

The first code implementation followed
https://www.kaggle.com/manikg/training-svm-classifier-with-hog-features/notebook
as a guideline for implementation.
"""

from sklearn import svm
import numpy as np
from CategoryLoader import CategoryLoader
from HOGFinder import HOGFinder

class DrawSVM:
    
    def __init__(self):
        self.svm = svm.SVC()
        self.cl = CategoryLoader()
        self.hf = HOGFinder()
        
    def train(self, cat, n=100):
        print("Initializing SVM training")
        # l = list(cat)
        data = self.cl.load(cat, n, 0, True)
        
        # Create both HOG Features and Label
        # SVM method requires data to be a (n_samples, m_features)
        # 2D array, so each row is a sample, and each column is a
        # specific feature.
        # It also requires a list of labels, (n_samples) corresponding
        # to each sample row in the data.
        print("Extracting HOG features and creating Labels")
        h_data = []
        h_labels = []
        for i in range(len(cat)):
            hogFeatures, _ = self.hf.findHOG(data[i])
            h_data.extend(hogFeatures)
            h_labels.extend([cat[i]]*len(hogFeatures))
           
        print("Hogfeatures Dim: ", len(hogFeatures))
        print("h_labels Dim: ", len(h_labels))
        hogFeatures = np.array(hogFeatures)
        data_frame = np.hstack(hogFeatures, h_labels)
        print("Data frame shape: ", data_frame.shape)
        
        
        

dsvm = DrawSVM()
dsvm.train((0,1,2), n=3)
