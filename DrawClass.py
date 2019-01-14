# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:50:39 2019

@author: heier
"""

# Imports
import sys
sys.path.insert(0, "ai/draw")
from CategoryLoader import CategoryLoader 
import numpy as np
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense, Activation


# Contains methods that handle data prep for classification
# Is independent of classifier used.
class DataPrep:
    def __init__(self):
        print("\nInitializing standard classification framework.")
        self.category_loader = CategoryLoader()
        # Note: the last element of data is its category.
        self.data = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
    
    # Loads data for the classifier of DrawProcess to use.
    
    # Only provides the data, does not split it into
    def load_data(self, cat, n, n_start=0, random=False):
        "\nload data in a single take"
        new_data = self.category_loader.load1D(cat, n, n_start, random)
        
        print("Creating labels")
        labels = []
        print("New data: ", len(new_data))
        print("shape: ", new_data[0].shape)
        for i in cat:
            labels.extend([cat[i]]*np.size(new_data[i],0))
        
        print("Attaching class to end of data.")
        new_data = np.array(new_data)
        new_data = np.reshape(new_data, (np.size(new_data, 0)*np.size(new_data,1), np.size(new_data,2)))
        labels = np.array(labels).reshape(len(labels), 1)
#        print("New data shape: ", new_data.shape)
#        print("Label shape: ", labels.shape)
        self.data = np.hstack((new_data, labels))
    
    def shuffle_data(self):
        np.random.shuffle(self.data)
    
    def split_data(self, split_percentage):
        print("\nSplit data into <x/y>_<train/test>")
        # Percentage training data
        percentage = 66
        partition = int(len(self.data)*percentage/100)
        
        # Split into training and test set
        self.x_train = self.data[:partition,:-1]
        self.x_test = self.data[partition:,:-1]
        self.y_train = self.data[:partition,-1:].ravel()
        self.y_test = self.data[partition:,-1:].ravel()
        
        print("x_train: ", self.x_train.shape)
        print("y_train: ", self.y_train.shape)
        print("x_test: ", self.x_test.shape)
        print("y_test: ", self.y_test.shape)
    
    
    # Loads data to be trained on directly. Does not update self.data.
    def load_training_data(self, cat, n, n_start, random=False):
        print("\nLoading only training data")
        new_data = self.category_loader.load1D(cat, n, n_start, random)
        
        print("Creating labels")
        labels = []
        for i in cat:
            labels.extend([cat[i]]*np.size(new_data[i],0))
        
        print("Creating training data")
        new_data = np.array(new_data)
        new_data = np.reshape(new_data, (np.size(new_data, 0)*np.size(new_data,1), np.size(new_data,2)))
        self.x_train = new_data
        labels = np.array(labels).reshape((len(labels),))
        self.y_train = labels
    
    
    # Loads data to be tested directly. Does not update self.data.
    def load_testing_data(self, cat, n, n_start, random=False):
        print("\nLoading only testing data")
        new_data = self.category_loader.load1D(cat, n, n_start, random)
        
        print("Creating labels")
        labels = []
        for i in cat:
            labels.extend([cat[i]]*np.size(new_data[i],0))
        
        print("Creating test data")
        new_data = np.array(new_data)
        new_data = np.reshape(new_data, (np.size(new_data, 0)*np.size(new_data,1), np.size(new_data,2)))
        self.x_test = new_data
        labels = np.array(labels).reshape((len(labels),))
        self.y_test = labels
        
    

# Classifier using Keras based neural network model.
# Note to self: Does keras tell apart y_label being (x,) and (x,1)? 
class DrawNN:
    def init(self):
        print("Initializing sequential neural network.")
        

# Classifier using SKLearn-based C-SVM model.
class DrawSVM:
    def init(self, categories):
        print("\nInitializing c support vector machine.")
        self.cat = categories
        # Starting basic structure. Change as needed.
        self.model = Sequential()
            self.model.add(Dense(100, input_dim=784))
            self.model.add(Activation('relu'))
            self.model.add(Dense(len(self.cat)))
            self.model.add(Actication('softmax'))
                
        ])
    
    def train(self):
        print("\nTraining with all the data.")
    
    def trainBatch(self):
        print("\nTraining with batch of data.")
        
    
        

# TEST CASE 1: Test case to check that data loading works alright. 
       
#dprep = DataPrep()
#dprep.load_data(range(5), 30)
#dprep.split_data(66.6)

#dprep = DataPrep()
#dprep.load_training_data(range(5),20, 10)
#dprep.load_testing_data(range(5), 10, 0)
#print("x_train: ", dprep.x_train.shape)
#print("y_train: ", dprep.y_train.shape)
#print("x_test: ", dprep.x_test.shape)
#print("y_test: ", dprep.y_test.shape)
#
#img = dprep.x_train[0]
#print(dprep.y_train[0])
#img.shape = (28,28)
#plt.imshow(img)

# END TEST CASE 1.