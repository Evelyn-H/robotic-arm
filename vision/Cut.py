# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt


img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\4.png')

#Turn image into grayscale
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Threshold image, cutoff between 1st and 2nd number
ret, thresh = cv2.threshold(imgray, 140, 255, 0)

#Create kernel for eroding and dilating
kernel = np.ones((7,7),np.uint8)

#This is only erosion, commented out
#thresh2 = cv2.erode(thresh,kernel,1)

#Erosion then Dilation
thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

#Find all contours
(_,contours,_) = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Find largest contour
largest = 0
largestContour = 0
for contour in contours:
    a = cv2.contourArea(contour)
    if(a>largest):
        largest = a
        largestContour = contour
        
#Make an angled rectangle, commented out for now
#box = cv2.boxPoints(rect)
#box = np.int0(box)
        
#Get bounding rectangle of largest contour
x,y,w,h = cv2.boundingRect(largestContour)

#Crop the image using largest contour
crop_img = img[y:y+h, x:x+w]
cv2.imwrite( "C:\\Users\\ekorz\\Desktop\\Project\\Images\\4.jpg", crop_img);

###################################################################################################

#Draw rectangle
#cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

#Draw contour
cv2.drawContours(img, contours, -1, (127,255,255), 3)

#Show image
cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

exit
