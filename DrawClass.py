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
    def __init__(self, max_data_n=10000):
        print("\nInitializing standard classification framework.")
        self.category_loader = CategoryLoader()
        # Note: the last element of data is its category.
        self.instances = max_data_n
        self.all_data = np.array(
                self.category_loader.load1D(range(24), 
                        self.instances, 0, False))
        self.all_data.shape = (24, self.instances, 784)
        self.data = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
    
    # Load from the loaded data.
    def load_from_all_data(self, cat, n, n_start):
        ar = np.zeros((len(cat),n,784), dtype=np.uint8)
        i = 0
        n_end = n_start+n
        for c in cat:
            ar[i,:,:] = self.all_data[c, n_start:n_end,:]
            i += 1
        
        return ar
    
    
    def shuffle_data(self):
        np.random.shuffle(self.data)
    
    
    # Loads data for the classifier of DrawProcess to use.
    # Only provides the data, does not split it into
    def load_data(self, cat, n, n_start=0, shuffle=False):
        # Can't load too much.
        if n > self.instances:
            return None
        
        # Load from all_data.
        new_data = self.load_from_all_data(cat, n, n_start)
        
        
        print("Creating labels")
        labels = []
        print("New data: ", new_data.shape)
        for i in range(len(cat)):
            labels.extend([cat[i]]*np.size(new_data,1))
        
        print("Attaching class to end of data.")
        new_data = new_data.reshape(
                (new_data.shape[0]*new_data.shape[1], 784))
        labels = np.array(labels).reshape(len(labels), 1)
#        print("New data shape: ", new_data.shape)
#        print("Label shape: ", labels.shape)
        self.data = np.hstack((new_data, labels))
        
        if shuffle:
            self.shuffle_data()
        # End.
        
    
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
    def load_training_data(self, cat, n, n_start):
        print("\nLoading only training data")
        new_data = self.load_from_all_data(cat, n, n_start)
        
        print("Creating labels")
        labels = []
        for i in range(len(cat)):
            labels.extend([cat[i]]*np.size(new_data,1))
        
        print("Creating training data")
        new_data = new_data.reshape(
                (new_data.shape[0]*new_data.shape[1], 784))
        self.x_train = new_data
        labels = np.array(labels).reshape((len(labels),))
        self.y_train = labels
    
    
    # Loads data to be tested directly. Does not update self.data.
    def load_testing_data(self, cat, n, n_start):
        print("\nLoading only testing data")
        new_data = self.load_from_all_data(cat, n, n_start)
        
        print("Creating labels")
        labels = []
        for i in range(len(cat)):
            labels.extend([cat[i]]*np.size(new_data,1))
        
        print("Creating test data")
        new_data = new_data.reshape(
                (new_data.shape[0]*new_data.shape[1], 784))
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
        self.model.add(Activation('softmax'))
    
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