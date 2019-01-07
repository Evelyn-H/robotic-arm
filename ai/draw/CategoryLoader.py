# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 12:02:59 2018

@author: heier
"""

import numpy
import random
from random import sample
from matplotlib import pyplot as plt
import cv2

class CategoryLoader:
    # Values needed to extract the different datatypes.
    def __init__(self): 
        self.file_path = "C:/Users/heier/Dropbox/Maastricht U/3.Project.1/"
        self.file_start = "full_numpy_bitmap_"
        self.file_type = ".npy"
        self.category = (
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
        
    def loadBitmap(self, filename):
        return numpy.load(filename)
        
    
    # load n images of inst type, converted into 2d array format.
    # if n is 0 or less, it loads all the images. In this case, if
    # random is true, the images will be shuffled in order.
    # if (n + n_start > #instances), it loops to the beginning.
    def loadSingle(self, inst, n, n_start, random):
        # We got an integer value
        bm = None
        if (isinstance(inst, int)):
            if 0 <= inst and inst < len(self.category):
                file = self.file_path + self.file_start + self.category[inst]
                file += self.file_type
                bm = self.loadBitmap(file)
            else:
                print("Error: outside category range")
                return None
        
        # Got string name to search with
        elif (isinstance(inst, str)):
            exists = False
            cat = -1
            for i in range(self.category):
                if self.category[i] == inst:
                    exists = True
                    cat = i
            if (exists): 
                file = self.file_path + self.file_start + self.category[cat]
                file += self.file_type
                bm = self.loadBitmap(file)
            else:
                print("Error: name given not in categories.")
                return None
                
        # Begin getting data.
        bm.shape = (len(bm), 28, 28)
        # Get all.
        if (n <= 0 or n >= len(bm)):
            print("Loading all images...")
            if (random):
                print("Shuffling.")
                numpy.random.shuffle(bm)
            return bm
        else: # Get n images
            print("Loading ", n, " images from " + self.category[inst] + "...")
            if random:
                # TODO: will not this change the outer
                # list datatype? Have to test.
                print("Random samples, no repetition")
                bm_new = numpy.zeros((n,28,28), numpy.uint8)
                samples = sample(range(len(bm)), n)
                
                bmi = 0
                
                for i in range(0, n):
                    bm_new[bmi, :, :] = bm[samples[i]];
                    bmi += 1
                
                return bm_new
            else: # non-random image list.
                bm_new = numpy.zeros((n, 28, 28), numpy.uint8)
                loop = False
                end = n_start + n
                end2 = 0
                
                if (n_start + n) >= numpy.size(bm, 0):
                    loop = True
                    end2 = end - numpy.size(bm, 0)
                    end = numpy.size(bm, 0)
                
                bmi = 0

                for i in range(n_start, end):
                    bm_new[bmi, :, :] = bm[i]
                    bmi += 1
                
                if (loop):
                    for i in range(0, end2):
                        bm_new[bmi, :, :] = bm[i]
                        bmi += 1
                
                return bm_new

    def loadAll(self, n, n_start, random):
        data = []
        for i in range(len(self.category)):
            data.append(self.loadSingle(i, n, n_start, random))
            
        return data
    
    def load(self, selection, n, n_start, random):
        data = []
        for i in selection:
            data.append(self.loadSingle(i, n, n_start, random))
            
        return data


    # Returns a drawing from a given category. Can specify
    # a specific element with pick, and give a specific set of 
    # drawings to choose from with pool.
    def singleImage(self, cat, pick=None, pool=None):
        print("Getting img ", cat, " from category ",
              self.category[cat])
        
        draw = None
        if not pool:
            if not pick:
                # No pool given, and no pick 
                # load randomly from a single category.
                draw = self.loadSingle(cat, 1, 0, True)[0]
            else:
                draw = self.loadSingle(cat, pick, 0, False)[0]
        else:
            # We do have a pool.
            # If no pick given, pick randomly.
            if not pick:
                pick = random.randint(0, len(pool)-1)
            draw = pool[pick]
        
        return draw
    
    def getPoints(img, mode="weighted")
        # Convert img to a graph
        # first, get vertices.
        v = []
        if mode=="weighted":
            # Weighted
            #   Find first white pixel, then draw in a continuous
            #   line going from adjacent pixels until none are left.
                        
                        
 
       
    def testCategoryLoader():
        cl = CategoryLoader()
        categories = [0, 5, 3, 8]
        data = cl.load(categories, 10, 0, False)
        print("Data has ", len(data), " categories")
        for i in range(len(categories)):
            print("Category: ", cl.category[categories[i]])
            
            cv2.imshow(cl.category[categories[i]], data[i][0])
            cv2.waitKey(0)
            cv2.destroyAllWindows()


# End
        