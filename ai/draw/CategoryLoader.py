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
            print("Loading all ", self.category[inst], " images...")
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
                print("Non-random sample")
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
    
    
    def loadSingle1D(self, inst, n, n_start, random):
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
                bm_new = numpy.zeros((n,784), numpy.uint8)
                samples = sample(range(len(bm)), n)
                
                bmi = 0
                
                for i in range(0, n):
                    bm_new[bmi, :] = bm[samples[i]];
                    bmi += 1
                
                return bm_new
            else: # non-random image list.
                print("Non-random sample")
                bm_new = numpy.zeros((n, 784), numpy.uint8)
                loop = False
                end = n_start + n
                end2 = 0
                
                if (n_start + n) >= numpy.size(bm, 0):
                    loop = True
                    end2 = end - numpy.size(bm, 0)
                    end = numpy.size(bm, 0)
                
                bmi = 0

                for i in range(n_start, end):
                    bm_new[bmi, :] = bm[i]
                    bmi += 1
                
                if (loop):
                    for i in range(0, end2):
                        bm_new[bmi, :] = bm[i]
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
    
    # Loads the data instances as 1D line of values.
    def load1D(self, selection, n, n_start, random):
        data = []
        for i in selection:
            data.append(self.loadSingle1D(i, n, n_start, random))
                
        return data


    # Returns a drawing from a given category. Can specify
    # a specific element with pick, and give a specific set of 
    # drawings to choose from with pool.
    def singleImage(self, cat, pick=None, pool=None):
        print("Getting img ", cat, " from category ",
              self.category[cat])
        
        draw = None
        if not pool:
            if pick==None:
                # No pool given, and no pick 
                # load randomly from a single category.
                draw = self.loadSingle(cat, 1, 0, True)[0]
            else:
                draw = self.loadSingle(cat, 1, pick, False)[0]
        else:
            # We do have a pool.
            # If no pick given, pick randomly.
            if not pick:
                pick = random.randint(0, len(pool)-1)
            draw = pool[pick]
        
        return draw
    
    
    def getSingleSurrounding(x, y, img):
        # deterministic
        for i in range(x-1,x+2):
            for j in range(y-1, y+2):
                # (i,j) is in drawing, and not the center pixel.
                if 0<=i and i<28 and 0<=j and j<28 and i!=x and j!=y:
                    if img[i,j]>0:
                        return (i,j)
        
        return None
    
    
    # Given an image, this finds a collection of lines
    # That approximate the drawing in the image.
    # Returns a list of lines.
    # Once you have called this method on an image, it is best to 
    # first call: 
    #   FormatConvert.scaleShift(drawing, shift=(-14,-14))
    # to center it. then you can watch the result with 
    #   draw=FormatConvert.filePointToImg(None, pl=points2); plt.imshow(draw)
    def getImagePoints(self, img, mode="simple", thresh_v=180):
        # Convert img to a graph
        if mode=="simple":
            # Do binary threshold, remaining pixels become "vertices"
            # in this drawing. drawing is done by finding a white pixel
            # among the surrounding pixels.
            _, t = cv2.threshold(img, thresh_v, 255, cv2.THRESH_BINARY)
            remaining = t.copy()
                        
            drawing = []
            
            for x in range(28):
                for y in range(28):
                    # Non empty pixel. Time to draw something.
                    if remaining[x,y] > 0:
                        line = [(y,x)]
                        
                        # investigate surrounding pixels.
                        remaining[x,y] = 0
                        vertex = CategoryLoader.getSingleSurrounding(x,y,remaining)
                        while vertex:
                            remaining
                            line.append((vertex[1], vertex[0]))
                            newX = vertex[0]
                            newY = vertex[1]
                            remaining[newX, newY] = 0
                            vertex = CategoryLoader.getSingleSurrounding(newX, newY, remaining)
                        
                        # Sub case, if only one pixel, add twice.
                        if len(line)==1:
                            line.append((y,x))
                        
                        drawing.append(line)
            # Finished drawing stuff.
                    
            return drawing
                        
                        
                        
                        
            
            
            
        # Below is way complicating it. Keeping code here for future ref.
#        if mode=="weighted":
#            # Weighted
#            #   Find first white pixel, then draw in a continuous
#            #   line going from adjacent pixels until none are left.
#            for x in range(0, 28, 2):
#                for y in range(0, 28, 2):
#                    # in cell format:
#                    #   p00 / p01
#                    #   p10 / p11
#                    p00 = img[x][y]
#                    p01 = img[x][y+1]
#                    p10 = img[x+1][y]
#                    p11 = img[x+1][y+1]
#                    
#                    # Only add a vertex if any have a value.
#                    if p00>0 or p01>0 or p10>0 or p11>0:
#                        # Relative total.
#                        tot = p00 + p01 + p10 + p11
#                        dx = float((p10+p11)-(p00+p01))/float(tot)
#                        dy = float((p01+p11)-(p00+p11))/float(tot)
#                        
#                        v.extend((x+1+dx, y+1+dy))
#            # Vertices gathered.
#            # Now to generate sequences of edges to become lines.
#            
#            # Still unfinished.
                    
                    
                        
                        
 
       
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
        