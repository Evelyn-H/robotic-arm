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
from os import listdir

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
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
            self.category_loader.load1D(range(10),
                                        self.instances, 0, False))
        self.all_data.shape = (10, self.instances, 784)
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
        partition = int(len(self.data) * split_percentage / 100)
        
        if split_percentage < 100:
            # Split into training and test set
            self.x_train = self.data[:partition, :-1]
            self.x_test = self.data[partition:, :-1]
            self.y_train = self.data[:partition, -1:].ravel()
            self.y_test = self.data[partition:, -1:].ravel()
    
            print("x_train: ", self.x_train.shape)
            print("y_train: ", self.y_train.shape)
            print("x_test: ", self.x_test.shape)
            print("y_test: ", self.y_test.shape)
        else:
            self.x_train = self.data[:partition, :-1]
            self.y_train = self.data[:partition, -1:].ravel()
            print("x_train: ", self.x_train.shape)
            print("y_train: ", self.y_train.shape)
            

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
        if self.x_test:
            self.x_test = scaler.transform(self.x_test)

    # Applies HOG to x_train and x_test
    def applyHOG(self, ppc=4, cpb=2):
        print("Extracting HOG features")
        self.x_train.shape = (len(self.x_train), 28, 28)
        
        if self.x_test:
            self.x_test.shape = (len(self.x_test), 28, 28)
        hf = HOGFinder()
        hf.ppc = ppc
        hf.cpb = cpb
        new_x_train = hf.findHOG2(self.x_train)
        
        if self.x_test:
            new_x_test = hf.findHOG2(self.x_test)

        self.x_train = new_x_train
        
        if self.x_test:
            self.x_test = new_x_test
     
        
    def loadImgData(self):
        size = 180
#        size2 = size*size
        folder = "drawn_images"
        # Load data
        imgList = listdir(folder)
        imgAr = np.zeros((109, size, size), dtype=np.uint8)
        imgCl = np.zeros((109,), dtype=np.uint8)
        img28 = np.zeros((109, 28, 28), dtype=np.uint8)
        
        # Add image
        for i,e, in enumerate(imgList):
            file = folder + "/" +e
            img = cv2.imread(file, 0)
            imgAr[i,:,:] = img[:,:]
        
        # Get category.
        for i, c, in enumerate(imgList):
            for j, cat in enumerate(self.category_loader.category):
                name = "_" + cat + "_"
                if c.find(name) > -1:
                    imgCl[i] = j
        
        # Preprocess The imgAr data into img28
        for i, e in enumerate(imgAr):
            # Close to make smaller
#            kernel = np.ones((3, 3), np.uint8)
#            imgAr[i] = cv2.erode(imgAr[i], kernel, iterations = 1)
            # Reduce edge space?
#            x1, y1 = 0, 0
#            x2, y2 = 180, 180
#            
#            x1_done, x2_done, y1_done, y2_done = False, False, False, False
#            
#            
#            for j in range(180):
#                if not (x1_done and x2_done and y1_done and y2_done):
#                    if not x1_done:
#                        for k in range(180):
#                            if imgAr[i,k,j] > 0:
#                                x1 = k
#                                x1_done = True
#                                break
#                    if not x2_done:
#                        for k in range(179,-1,-1):
#                            if imgAr[i,k,j] > 0:
#                                x2 = k
#                                x2_done = True
#                                break
#                    if not y1_done:
#                        for k in range(180):
#                            if imgAr[i,j,k] > 0:
#                                y1 = k
#                                y1_done = True
#                                break
#                    if not y2_done:
#                        for k in range(179,-1,-1):
#                            if imgAr[i,j,k] > 0:
#                                y2 = k
#                                y2_done = True
#                                break
#                else:
#                    break
#            print("\n(i,j,k) = (", i, ", ", j, ", ", k, ")")
#            print("x1: ", x1, "\tx2: ", x2)
#            print("y1: ", y1, "\ty2: ", y2)
#            print(imgAr[i])
#            input()
#            # Have defined margin.
#            margin = 10
#            if x1 < margin:
#                x1 = 0
#            else:
#                x1 -= margin
#            
#            if x2 > 180-margin:
#                x2 = 180
#            else:
#                x2 += margin
#            
#            if y1 < margin:
#                y1 = 0
#            else:
#                y1 -= margin
#                
#            if y2 > 180-margin:
#                y2 = 180
#            else:
#                y2 += margin
#            
#            dx = x2 - x1
#            dy = y2 - y1
#            
#            if dx < 180 or dy < 180:
#                if dx > dy:
#                    diff = (dx-dy)/2
#                    y1 = max((y1-diff, 0))
#                    y2 = min((y2+diff, 180))
#                if dy > dx:
#                    diff = (dy-dx)/2
#                    x1 = max((x1-diff, 0))
#                    x2 = min((x2+diff, 0))
#            img2 = imgAr[i, x1:x2, y1:y2]
#            img2 = cv2.blur(img2, (5,5))
            
            imgAr[i] = cv2.blur(imgAr[i], (5,5))
            img28[i] = cv2.resize(imgAr[i], (28,28))
        
        img28.shape = (109, 784)
        
        return img28, imgCl
            


# Classifier using Keras based neural network model.
# Note to self: Does keras tell apart y_label being (x,) and (x,1)?
class DrawSVM:
    def __init__(self, categories):
        print("\nInitializing c support vector machine.")
        self.svm = svm.LinearSVC()
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
    def __init__(self, categories, inp_size=784):
        print("Initializing sequential neural network.")
        self.cat = categories
        # Starting basic structure. Change as needed.
        self.model = Sequential()
        self.model.add(Dense(250, activation='relu', input_dim=inp_size))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(self.cat), activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='sparse_categorical_crossentropy',
                           optimizer=sgd,
                           metrics=['accuracy'])

    def train_model(self, x_train, y_train):
        print("\nTraining with all the data.")
        self.model.fit(x_train, y_train, epochs=30, batch_size=100)

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
        self.categories = (
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

    def GetResults(self, y_predicted, y_test, opt_msg="", fname=""):
        print("Accuracy: " + str(accuracy_score(y_test, y_predicted)))
        print('\n')
        print(classification_report(y_test, y_predicted))

        print("Confusion matrix:")
        c_matrix = confusion_matrix(y_test, y_predicted)
        norm_c_matrix = np.array(c_matrix, dtype=np.float64)
        norm_sum = np.sum(norm_c_matrix)
        norm_c_matrix = np.divide(norm_c_matrix, norm_sum)
        norm_c_matrix = np.multiply(norm_c_matrix, 100)
        size = 12
        n_classes = len(c_matrix)
        Labels = self.categories[0:n_classes]
        
        plt.figure(figsize=(size, size))
        plt.imshow(
            norm_c_matrix, 
            interpolation='nearest', 
            cmap=plt.cm.Blues)
        title = "Confusion matrix \n(normalised to % of total test data)"
        if opt_msg:
            title = opt_msg + ", " + title
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(n_classes)
        plt.xticks(tick_marks, Labels, rotation=90)
        plt.yticks(tick_marks, Labels)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        
        if fname:
            plt.savefig(fname)
        else:
            plt.show()
            

    def testNN(self, cat_n=10, data_n=2000):
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n, 0)
        dp.shuffle_data()
        dp.split_data(100)

        # Feature scaling fucks up the HOG. Use only one, but not both.
        dp.applyHOG(ppc=7, cpb=2)
        dp.feature_scale_data()

        nn = DrawNN(range(cat_n), inp_size=len(dp.x_train[0]))
        nn.train_model(dp.x_train, dp.y_train)

#        print("\nUsing sklearn...")
        # Get best prediction.
#        y_p = nn.predict_model(dp.x_test)
#
#        self.GetResults(y_p, dp.y_test)
        nn.model.save("nn_hog.h5")
        

    def testSVM(self, cat_n=10, data_n=1000, C_val=0.5):
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n, 0)
        dp.shuffle_data()
        dp.split_data(80)

        # Feature scaling fucks up the HOG. Use only one, but not both.
        dp.applyHOG()
        dp.feature_scale_data()

        svm = DrawSVM(range(cat_n))
        svm.svm.C = C_val
        svm.train_model(dp.x_train, dp.y_train)
        y_p = svm.predict_model(dp.x_test)

        self.GetResults(y_p, dp.y_test)

    def testSVM_C_param(self, cat_n=10, data_n=2000):
        C_param = [5, 6, 7, 8, 9]
        
        # Prep all Data
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n, 0)
        dp.shuffle_data()
        dp.split_data(80)

        dp.applyHOG()
        dp.feature_scale_data()
        
        svm = DrawSVM(range(cat_n))
        
        for c in C_param:
            print("\nc is: ", c)
            svm.svm.C = c
            svm.train_model(dp.x_train, dp.y_train)
            y_p = svm.predict_model(dp.x_test)
    
            msg_text = "C = " + str(c)
            file = "test" + str(c) + ".png"
            self.GetResults(y_p, dp.y_test, fname=file, 
                            opt_msg=msg_text)
            

    # Data_n corresponds to training data.
    def testOnReal(self, data_n=1000):
        cat_n = 10
        dp = DataPrep(max_data_n=data_n)
        dp.load_data(range(cat_n), data_n)
        dp.shuffle_data()
        dp.split_data(100)
        
        # Prepare test data.
        dp.x_test, dp.y_test = dp.loadImgData()
        dp.applyHOG()
        dp.feature_scale_data()
        
        # Test on NN
        nn = DrawNN(range(cat_n))
        nn.train_model(dp.x_train, dp.y_train)
        
        # Print results
        y_p_raw = nn.predict_model(dp.x_test)

        self.GetResults(y_p_raw, dp.y_test)
        
        # Test on LinearSVC, Prep test data first
#        svm = DrawSVM(range(cat_n))
#        svm.train_model(dp.x_train, dp.y_train)
#        y_p = svm.predict_model(dp.x_test)
#
#        self.GetResults(y_p, dp.y_test)
        
        
        

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
#        boundFile = "bounds.txt"

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
