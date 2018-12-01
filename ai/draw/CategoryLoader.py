# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 12:02:59 2018

@author: heier
"""

import numpy
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
            print("Loading ", n, " images...")
            if random:
                # TODO: will not this change the outer
                # list datatype? Have to test.
                print("Random samples, no repetition")
                bm_r = random.sample(n)
                return bm_r
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
                
                
            
# For next: Debug the loop thing, see that it works both with
# with and without random.
catN = 0
img_n = 0
start = 5
r = True
cl = CategoryLoader()
ar = cl.loadSingle(catN, img_n, start, r)
print(ar.shape)

img = 0
cv2.imshow(cl.category[catN], ar[img])
cv2.waitKey(0)
cv2.destroyAllWindows()







# End
        