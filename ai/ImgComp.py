# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:45:38 2018

@author: heier
"""

from draw.CategoryLoader import CategoryLoader
import numpy as np
import cv2
from FormatConvert import FormatConvert
from matplotlib import pyplot as plt
from skimage.measure import compare_ssim

# Abstract class meant for any kind of image comparison tasks
class ImgComp:
    
    def __init__(self):
        self.orb = cv2.ORB_create()
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        self.flann = cv2.FlannBasedMatcher(index_params,search_params)
        self.bf = cv2.BFMatcher()   
    
    # Uses
    def compareSSIM(img1, img2, rollDist=5):
        if (isinstance(img1, str)):
            img1 = ImgComp.preprocess(img1, gausN=20)
        else:
            img1 =ImgComp.preprocessImg(img1, gausN=20)     
            
        if (isinstance(img2, str)):
            img2 = ImgComp.preprocess(img2, gausN=20)
        else:
            img2 =ImgComp.preprocessImg(img2, gausN=20)
        
        
        img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))
        
        bestMatch = -1
        
        np.roll(img1, -rollDist, axis=0)
        np.roll(img1, -rollDist, axis=1)
        
        # shift.
        for i in range(rollDist*2):
            for j in range(rollDist*2):
                current = compare_ssim(img1, img2)
                if (current > bestMatch):
                    bestMatch = current
                
                np.roll(img1, 1, axis=0)
            np.roll(img1, 1, axis=1)
                
                
        
        return bestMatch
     
    # Takes a filename of an image (jpg, png, etc.) that
    # the preprocessing step is applied to.
    def preprocess(imgFile, tVal=127, gausN=20):
        imgLoaded = cv2.imread(imgFile, 0) # grayscale
        _, thresh = cv2.threshold(imgLoaded, tVal, 255, 
                                  cv2.THRESH_BINARY_INV)

        blur = thresh
        for i in range(gausN):    
            b1 = cv2.GaussianBlur(blur,(9,9),0)
            blur = np.maximum(b1, thresh)
        return blur
    
    # Takes a 2d numpy uint8 array as an argument and 
    # applies the preprocessing step to it.
    def preprocessImg(img, tVal=127, gausN=20):
        # Turn to grayscale if already in colour.
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
        _, thresh = cv2.threshold(img, tVal, 255, 
                                  cv2.THRESH_BINARY)
        
        
        blur = thresh
        for i in range(gausN):    
            b1 = cv2.GaussianBlur(blur,(9,9),0)
            blur = np.maximum(b1, img)
        return blur
    
    # Compare two 2D images.
    # This does not work for small images. Argh!
    def compareORB(self, img1, img2):
        print("Comparing two 2D with ORB")
        kp1, des1 = self.orb.detectAndCompute(img1, None)
        kp2, des2 = self.orb.detectAndCompute(img2, None)
        
#        des1 = np.asarray(des1, np.float32)
#        des2 = np.asarray(des2, np.float32)
#        matches = self.flann.knnMatch(des1, des2, k=2)
        matches = self.bf.knnMatch(des1,des2, k=2)
        
        good = []
        for m,n in matches:
            if m.distance < 0.65*n.distance:
                good.append([m])
        
        print("Des1 size: ", len(des1))
        print("Des2 size: ", len(des2))
        print("Good size: ", len(good))
        
        # cv2.drawMatchesKnn expects list of lists as matches.
        img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
        plt.imshow(img3), plt.show()
        
        return len(good), len(des1), len(des2)
        
    
    # Currently only set to TM_SQDIFF.
    # Only other option is potentially TM_SQDIFF_NORM
    # As they kind of work like errors in that 0 
    # is completely equal.
    # Assumes grayscale uint8 numpy 2d array
    # This does not appear to work well at all, sadly.
#    def compareTemplateMatching(img1, img2):
#        print("Comparing two 2D images using Template Matching")
#        i1c = img1.copy()
#        i2c = img2.copy()
#        cv2.GaussianBlur(i1c, (7,7), 0)
#        cv2.GaussianBlur(i2c, (7,7), 0)
#        res = cv2.matchTemplate(i1c, i2c, cv2.TM_SQDIFF)
#        minVal, _, _, _ = cv2.minMaxLoc(res)
#        
#        print("Min-val found: " , minVal)
#        return minVal
        
    
#    def testComp(selection, n):
#        cl = CategoryLoader()
#        data = cl.load(selection, n, 0, False)
#        
#        size = len(selection)
#        
#        md = np.zeros((size, size, 3), dtype=np.float64)
#        
#        # Go through all categories
#        for cati in range(size):
#            for catj in range(size):
#                
#                # Go through each image in each category.
#                for imgk in range(n):
#                    for imgl in range(n):
#                        img1 = data[cati][imgk]
#                        img2 = data[catj][imgl]
#                        # Template matching
#                        # IMAGES NEED TO BE OF SAME SIZE
#                        val = ImgComp.compareSSIM(img1, img2)
#                        
#                        
#                        c = md[cati, catj, 0]
#                        m = md[cati, catj, 1]
#                        ma = md[cati, catj, 2]
#                        count, mean, M2 = ImgComp.update(c, m, ma, val)
#                        md[cati, catj, 0] = count
#                        md[cati, catj, 1] = mean
#                        md[cati, catj, 2] = M2
#        
#        # Finalize
#        final = np.zeros((size,size), dtype=np.float64)
#        for i in range(size):
#            for j in range(size):
#                mf, _, _ = ImgComp.finalize(md[i, j, 0], md[i, j, 1], md[i, j, 2])
#                final[i,j] = mf
#                            
#        print(final)
                
        
#    # Welford's online algorithm below, copied from wikipedia
#    # for a new value newValue, 
#    # compute the new count, new mean, the new M2.
#    # mean accumulates the mean of the entire dataset
#    # M2 aggregates the squared distance from the mean
#    # count aggregates the number of samples seen so far
#    def update(count, mean, M2, newValue):
#        count += 1 
#        delta = newValue - mean
#        mean += delta / count
#        delta2 = newValue - mean
#        M2 += delta * delta2
#    
#        return count, mean, M2
#    
#    # retrieve the mean, variance and sample variance from an aggregate
#    def finalize(count, mean, M2):
#        (mean, variance, sampleVariance) = (mean, M2/count, M2/(count - 1)) 
#        if count < 2:
#            return float('nan')
#        else:
#            return mean, variance, sampleVariance
    
    def tinyRoll(imgToRoll, rollDist):
        img = imgToRoll.copy()
        for i in range(img.shape[0]):
            if i%2 == 0:
                img[i] = np.roll(img[i], rollDist)
            else:
                img[i] = np.roll(img[i], -rollDist)
        
        return img
    
    def test2(comparer):
        fbase = "C:/Users/heier/Desktop/robotic-arm/ai/ice_"
        ls = []
        # Load image files.
        for i in range(10):
            fn = fbase + "0" + str(i) +".jpg"
            ls.append(ImgComp.preprocess(fn))
        
        # Compare with given img image.
        img1 = ls[comparer]
        print("Img1 shape: ", img1.shape)
        for i in range(len(ls)):
            img2r = cv2.resize(ls[i], dsize=(img1.shape[1], img1.shape[0]))
            c = compare_ssim(img1, img2r)
            print(i, " - SSIM: ", c)
            
            
        

f00 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_00.jpg"
f01 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_01.jpg"
f02 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_02.jpg"
f03 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_03.jpg"
f04 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_04.jpg"
f05 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_05.jpg"
f06 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_06.jpg"
f07 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_07.jpg"
f08 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_08.jpg"
f09 = "C:/Users/heier/Desktop/robotic-arm/ai/ice_09.jpg"

fd00 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_1234.png"
fd01 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_airplane.png"
fd02 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_backpack.png"
fd03 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_cactus.png"
fd04 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_dog.png"
fd05 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_ear.png"
fd06 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_face.png"
fd07 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_garden.png"
fd08 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_hamburger.png"
fd09 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_icecream.png"
fd10 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/draw_jacket.png"

# Drawings done by robot
pf00 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/1.png"
pf01 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/2.png"
pf02 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/3.png"
pf03 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/4.png"
pf04 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/5.png"
pf05 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/6.png"
pf06 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/7.png"
pf07 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/8.png"
pf08 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/9.png"
pf09 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/10.png"
pf10 = "C:/Users/heier/Desktop/robotic-arm/ai/drawn_images/11.png"

pi00 = ImgComp.preprocess(pf00, gausN=0, tVal=80)
pi01 = ImgComp.preprocess(pf01, gausN=0, tVal=80)
pi02 = ImgComp.preprocess(pf02, gausN=0, tVal=80)
pi03 = ImgComp.preprocess(pf03, gausN=0, tVal=80)
pi04 = ImgComp.preprocess(pf04, gausN=0, tVal=80)
pi05 = ImgComp.preprocess(pf05, gausN=0, tVal=80)
pi06 = ImgComp.preprocess(pf06, gausN=0, tVal=80)
pi07 = ImgComp.preprocess(pf07, gausN=0, tVal=80)
pi08 = ImgComp.preprocess(pf08, gausN=0, tVal=80)
pi09 = ImgComp.preprocess(pf09, gausN=0, tVal=80)
pi10 = ImgComp.preprocess(pf10, gausN=0, tVal=80)

pi00 = pi00[270:525, 395:605]
pi01 = pi01[175:535, 350:660]
pi02 = pi02[175:530, 350:660]
pi03 = pi03[120:550, 330:645]
pi04 = pi04[225:620, 320:700]
pi05 = pi05[210:500, 410:610]
pi06 = pi06[175:555, 345:655]
pi07 = pi07[75:525, 130:885]
pi08 = pi08[210:495, 265:695]
pi09 = pi09[140:570, 340:630]
pi10 = pi10[130:600, 210:755]

pi00 = ImgComp.preprocessImg(pi00)
pi01 = ImgComp.preprocessImg(pi01)
pi02 = ImgComp.preprocessImg(pi02)
pi03 = ImgComp.preprocessImg(pi03)
pi04 = ImgComp.preprocessImg(pi04)
pi05 = ImgComp.preprocessImg(pi05)
pi06 = ImgComp.preprocessImg(pi06)
pi07 = ImgComp.preprocessImg(pi07)
pi08 = ImgComp.preprocessImg(pi08)
pi09 = ImgComp.preprocessImg(pi09)
pi10 = ImgComp.preprocessImg(pi10)

# Line files for robot
t00 = "C:/Users/heier/Desktop/robotic-arm/ai/l_1234.txt"
t01 = "C:/Users/heier/Desktop/robotic-arm/ai/l_airplane.txt"
t02 = "C:/Users/heier/Desktop/robotic-arm/ai/l_backpack.txt"
t03 = "C:/Users/heier/Desktop/robotic-arm/ai/l_cactus.txt"
t04 = "C:/Users/heier/Desktop/robotic-arm/ai/l_dog.txt"
t05 = "C:/Users/heier/Desktop/robotic-arm/ai/l_ear.txt"
t06 = "C:/Users/heier/Desktop/robotic-arm/ai/l_face.txt"
t07 = "C:/Users/heier/Desktop/robotic-arm/ai/l_garden.txt"
t08 = "C:/Users/heier/Desktop/robotic-arm/ai/l_hamburger.txt"
t09 = "C:/Users/heier/Desktop/robotic-arm/ai/l_icecream.txt"
t10 = "C:/Users/heier/Desktop/robotic-arm/ai/l_jacket.txt"

li00 = FormatConvert.filePointToImg(t00, scale=(2.4,2.4), borderWindow=50)
li01 = FormatConvert.filePointToImg(t01, scale=(2.4,2.4), borderWindow=50)
li02 = FormatConvert.filePointToImg(t02, scale=(2.4,2.4), borderWindow=50)
li03 = FormatConvert.filePointToImg(t03, scale=(2.4,2.4), borderWindow=50)
li04 = FormatConvert.filePointToImg(t04, scale=(2.4,2.4), borderWindow=50)
li05 = FormatConvert.filePointToImg(t05, scale=(2.4,2.4), borderWindow=50)
li06 = FormatConvert.filePointToImg(t06, scale=(2.4,2.4), borderWindow=50)
li07 = FormatConvert.filePointToImg(t07, scale=(2.4,2.4), borderWindow=50)
li08 = FormatConvert.filePointToImg(t08, scale=(2.4,2.4), borderWindow=50)
li09 = FormatConvert.filePointToImg(t09, scale=(2.4,2.4), borderWindow=50)
li10 = FormatConvert.filePointToImg(t10, scale=(2.4,2.4), borderWindow=50)

li00 = ImgComp.preprocessImg(li00)
li01 = ImgComp.preprocessImg(li01)
li02 = ImgComp.preprocessImg(li02)
li03 = ImgComp.preprocessImg(li03)
li04 = ImgComp.preprocessImg(li04)
li05 = ImgComp.preprocessImg(li05)
li06 = ImgComp.preprocessImg(li06)
li07 = ImgComp.preprocessImg(li07)
li08 = ImgComp.preprocessImg(li08)
li09 = ImgComp.preprocessImg(li09)
li10 = ImgComp.preprocessImg(li10)

a1 = []
#a2 = []
for i in range(11): #pi
    print("!")
    a1.append([])
#    a2.append([])
    for j in range(11): #li
        pix = vars()['pi'+str((int(i/10)))+str(i%10)]
        lix = vars()['li'+str((int(j/10)))+str(j%10)]
        v1 = ImgComp.compareSSIM(pix, lix, rollDist=5)
#        v2 = ImgComp.compareSSIM(pix, lix, rollDist=5)
        a1[len(a1)-1].append(v1)
#        a2[len(a2)-1].append(v2)
        print(".")
    
    for k in range(len(a1[len(a1)-1])):
        print(a1[len(a1)-1][k])
#    print(a2[len(a2)-2])



