# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 14:15:37 2018

@author: heier
"""

import cv2
import numpy

# Testing how to load one of the bitmaps of numpy.
name = "C:/Users/heier/Dropbox/Maastricht U/3.Project.1/full_numpy_bitmap_angel.npy"

x = numpy.load(name)

a1 = x[8,:];
a1.shape = (-1, 28)

#resize and threshold
big_a1 = cv2.resize(a1, (0,0), fx=1, fy=1)
ret, thresh = cv2.threshold(big_a1, 160, 255, cv2.THRESH_BINARY)
thresh_a1 = thresh.copy()

cv2.imshow('Ant', thresh_a1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Contours
_, contours, hierarchy = cv2.findContours(thresh_a1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
print("Number of contours found: " + str(len(contours)))

colora1 = cv2.cvtColor(thresh_a1, cv2.COLOR_GRAY2BGR)

for c in contours:
    accuracy = 0.01*cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, accuracy, True)
    cv2.drawContours(colora1, [approx], 0, (0, 255, 0), 1)

cv2.imshow('img with contours', colora1)
cv2.waitKey(0)
cv2.destroyAllWindows()
