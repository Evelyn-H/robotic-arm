# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 09:20:16 2018

@author: heier

The first code implementation followed
https://www.kaggle.com/manikg/training-svm-classifier-with-hog-features/notebook
as a guideline for implementation.
"""

from sklearn import svm
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
from CategoryLoader import CategoryLoader
from HOGFinder import HOGFinder

class DrawSVM:
    
    def __init__(self):
        self.svm = svm.SVC(C=1, gamma=0.5)
        self.cl = CategoryLoader()
        self.hf = HOGFinder()
        
    def train(self, cat, n=100):
        print("Initializing SVM training")
        # l = list(cat)
        data = self.cl.load(cat, n, 0, False)
        
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
            hogFeatures = self.hf.findHOG(data[i], False)
            h_data.extend(hogFeatures)
            h_labels.extend([cat[i]]*len(hogFeatures))
        
        print("Prepping data")
        h_data = np.array(h_data)
        h_labels = np.array(h_labels).reshape(len(h_labels), 1)
        print("Hogfeatures Dim: ", h_data.shape)
        print("h_labels Dim: ", h_labels.shape)
        data_frame = np.hstack((h_data, h_labels))

        
        print("Data frame shape: ", data_frame.shape)
        np.random.shuffle(data_frame) # Shuffle shuffle yo
        
        # Percentage training data
        percentage = 80
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
        print("First y_train element: ", y_train[0])
        
        print("Training SVM")
        self.svm.fit(x_train, y_train)
        print("Predicting test set")
        y_pred = self.svm.predict(x_test)
        
        print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
        print('\n')
        print(classification_report(y_test, y_pred))
        
        
        
