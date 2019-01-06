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
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix


class DrawMLP:
    
    def __init__(self):
        self.mlp = MLPClassifier(hidden_layer_sizes=(10),
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
        
        # Percentage training data
        percentage = 66
        partition = int(len(h_data)*percentage/100)
        
        # Split into training and test set
        x_train = data_frame[:partition,:-1]
        x_test = data_frame[partition:,:-1]
        y_train = data_frame[:partition,-1:].ravel()
        y_test = data_frame[partition:,-1:].ravel()
        
        print("x_train: ", x_train.shape)
        print("y_train: ", y_train.shape)
        print("x_test: ", x_test.shape)
        print("y_test: ", y_test.shape)
        
        print("Training MLP")
        self.mlp.fit(x_train, y_train)
        print("Predicting test set")
        y_pred = self.mlp.predict(x_test)
        
        print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
        print('\n')
        print(classification_report(y_test, y_pred))
        
        print("Confusion matrix:")
        print(confusion_matrix(y_test, y_pred))
        print("\n")
        
    
    # Consider: Should this also do feature scalling? Revisit at another point.
    def convert_to_1D(self, data):
        data.shape = (data.shape[0], 784)
        return data