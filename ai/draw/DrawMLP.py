# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 16:55:57 2019

@author: heier

Multi-Layer Perceptron, running on raw pixel features of image.
"""

# imports
import numpy as np
from sklearn.neural_network import MLPClassifier
from CategoryLoader import CategoryLoader

class DrawMLP:
    
    def __init__(self):
        self.mlp = MLPClassifier(hidden_layer_sizes=(100),
                                 random_state=1)
        self.cl = CategoryLoader()
        
    
    def train(self, cat, n=100):
        print("Initializing MLP training...")
        # Get data
        data = self.cl.load(cat, n, 0, False)
        
        print("Reverting to 1D array and creating Labels")
        h_data = []
        h_labels = []
        for i in range(len(cat)):
            data_1D = self.convert_to_1D(data[i])
            h_data.extend(data_1D)
            h_labels.extend([cat[i]]*len(data_1D))
        
        print("Prepping data")
        h_data = np.array(h_data)
        h_labels = np.array(h_labels).reshape(len(h_labels), 1)
        print("Image Dim: ", h_data.shape)
        print("h_labels Dim: ", h_labels.shape)
        data_frame = np.hstack((h_data, h_labels))
        
        print("Data frame shape: ", data_frame.shape)
        np.random.shuffle(data_frame) # Shuffle shuffle yo
    
    def convert_to_1D(self, data):
        for i in data:
            i.shape = (784)
        
        return data