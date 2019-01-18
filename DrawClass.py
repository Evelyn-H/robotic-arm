# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:50:39 2019

@author: heier
"""

# Imports
import sys
import cv2
sys.path.insert(0, "ai/draw")
from CategoryLoader import CategoryLoader
import numpy as np
from matplotlib import pyplot as plt
from ai import FormatConvert
from ai.draw.HOGFinder import HOGFinder
from sklearn import svm

# from keras.models import Sequential
# from keras.layers import Dense, Dropout, Activation
# from keras.optimizers import SGD
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from vision import Vision


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
        ar = np.zeros((len(cat), n, 784), dtype=np.uint8)
        i = 0
        n_end = n_start + n
        for c in cat:
            ar[i, :, :] = self.all_data[c, n_start:n_end, :]
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
            labels.extend([cat[i]] * np.size(new_data, 1))

        print("Attaching class to end of data.")
        new_data = new_data.reshape(
            (new_data.shape[0] * new_data.shape[1], 784))
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
        partition = int(len(self.data) * percentage / 100)

        # Split into training and test set
        self.x_train = self.data[:partition, :-1]
        self.x_test = self.data[partition:, :-1]
        self.y_train = self.data[:partition, -1:].ravel()
        self.y_test = self.data[partition:, -1:].ravel()

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
            labels.extend([cat[i]] * np.size(new_data, 1))

        print("Creating training data")
        new_data = new_data.reshape(
            (new_data.shape[0] * new_data.shape[1], 784))
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
            labels.extend([cat[i]] * np.size(new_data, 1))

        print("Creating test data")
        new_data = new_data.reshape(
            (new_data.shape[0] * new_data.shape[1], 784))
        self.x_test = new_data
        labels = np.array(labels).reshape((len(labels),))
        self.y_test = labels

    def feature_scale_data(self):
        # Taken from recommended practice for SKLearn.
        scaler = StandardScaler()
        # Don't cheat - fit only on training data
        scaler.fit(self.x_train)
        self.x_train = scaler.transform(self.x_train)
        # apply same transformation to test data
        self.x_test = scaler.transform(self.x_test)

    # Applies HOG to x_train and x_test
    def applyHOG(self):
        print("Extracting HOG features")
        self.x_train.shape = (len(self.x_train), 28, 28)
        self.x_test.shape = (len(self.x_test), 28, 28)
        hf = HOGFinder()
        new_x_train = hf.findHOG2(self.x_train)
        new_x_test = hf.findHOG2(self.x_test)

        self.x_train = new_x_train
        self.x_test = new_x_test


# Classifier using Keras based neural network model.
# Note to self: Does keras tell apart y_label being (x,) and (x,1)?
class DrawSVM:
    def __init__(self, categories):
        print("\nInitializing c support vector machine.")
        self.svm = svm.LinearSVC(C=5)
        self.cat = categories
        self.hf = HOGFinder()

    def train_model(self, x_train, y_train):
        print("\nTraining SVM")
        self.svm.fit(x_train, y_train)

    def predict_model(self, x_test):
        print("\nTesting model.")
        return self.svm.predict(x_test)


# Classifier using SKLearn-based C-SVM model.
class DrawNN:
    def __init__(self, categories):
        print("Initializing sequential neural network.")
        self.cat = categories
        # Starting basic structure. Change as needed.
        self.model = Sequential()
        self.model.add(Dense(500, activation='relu', input_dim=784))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(self.cat), activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='sparse_categorical_crossentropy',
                           optimizer=sgd,
                           metrics=['accuracy'])

    def train_model(self, x_train, y_train):
        print("\nTraining with all the data.")
        self.model.fit(x_train, y_train, epochs=20, batch_size=1000)

    def predict_model(self, x_test):
        print("\nTesting model.")
        y_pred = self.model.predict(x_test)
        y_p = np.zeros((len(y_pred),), dtype=np.uint8)
        for i in range(len(y_pred)):
            max = 0
            for j in range(len(y_pred[i])):
                if y_pred[i][max] < y_pred[i][j]:
                    max = j
            y_p[i] = max

        return y_p

# Testing stuff in this.


class DrawTest:
    def __init__(self, arm):
        self.arm = arm

    def GetResults(self, y_predicted, y_test):
        print("Accuracy: " + str(accuracy_score(y_test, y_predicted)))
        print('\n')
        print(classification_report(y_test, y_predicted))

        print("Confusion matrix:")
        print(confusion_matrix(y_test, y_predicted))
        print("\n")

    def testNN(self, cat_n=10, data_n=1000):
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n, 0)
        dp.shuffle_data()
        dp.split_data(80)

        # Feature scaling fucks up the HOG. Use only one, but not both.
        dp.feature_scale_data()
#        dp.applyHOG()

        nn = DrawNN(range(cat_n))
        nn.train_model(dp.x_train, dp.y_train)

        print("\nUsing sklearn...")
        # Get best prediction.
        y_p = nn.predict_model(dp.x_test)

        self.GetResults(y_p, dp.y_test)

    def testSVM(self, cat_n=10, data_n=1000):
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n, 0)
        dp.shuffle_data()
        dp.split_data(80)

        # Feature scaling fucks up the HOG. Use only one, but not both.
#        dp.feature_scale_data()
        dp.applyHOG()

        svm = DrawSVM(range(cat_n))
        svm.train_model(dp.x_train, dp.y_train)
        y_p = svm.predict_model(dp.x_test)

        self.GetResults(y_p, dp.y_test)

    def saveImgFromCamera(self, n, cat, fname_start):
        # dp = DataPrep(max_data_n=100)
        categories = (
                'airplane',
                'backpack',
                'cactus',
                'dog',
                'ear',
                'face',
                'garden',
                'hamburger',
                'icecream',
                'jacket',
                'kangaroo',
                'ladder',
                'mailbox',
                'nail',
                'ocean',
                'paintbrush',
                'rabbit',
                'sailboat',
                'table',
                'underwear',
                'vase',
                'windmill',
                'yoga',
                'zebra',
                )
        print('.')
        v = Vision()
        print('.')
        print("Beginning saving doodles from image.")
        print("First: Drawing bounds for doodle.")
        boundFile = "bounds.txt"

        print("Now for the drawing part!")
        for a in range(n):
            for i in cat:
                # self.arm.move_back()
                # FormatConvert.drawFromFile(boundFile, self.arm, speed=3)
                # self.arm.move_away()
                print("\nPlease draw ", categories[i], "...")
                input()
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = v._getImage(v.cam1)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
                img = np.rot90(img, 3)
                img = img[630:810, 260:440]
                name = fname_start + "_" + categories[i]
                name = name + "_" + str(a) + ".png"
                # cv2.imshow('frame', img)
                # cv2.waitKey(1)
                print("Saving name...")
                cv2.imwrite(name, img)
                print("Saved.")
                # input("next?")

        print("Done saving images.")


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
