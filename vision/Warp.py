# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 21:28:21 2018

@author: ekorz
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt

#Read cropped image
img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\4.jpg')

#Turn into grayscale
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Threshold
ret, thresh = cv2.threshold(imgray, 140, 255, 0)

#Kernel for noise filtering
kernel = np.ones((7,7),np.uint8)

#Noise filtering
#thresh2 = cv2.erode(thresh,kernel,1)
thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

#Find corners
dst = cv2.cornerHarris(thresh2,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
ret, treshH = ret, thresh = cv2.threshold(dst, 0, 255, 0)

#Get an array with all points
points = np.transpose(np.nonzero(treshH))

#Find corners closest to edges
highest1 = -10000
highest2 = -10000
highest3 = -10000
highest4 = -10000

for x in points:
    a=x[0]+x[1]
    b=x[0]-x[1]
    c=x[1]-x[0]
    d=-x[0]-x[1]
    if(a>highest1):
        highest1 = a
        BottomRight = x
    if(b>highest2):
        highest2 = b
        BottomLeft = x
    if(c>highest3):
        highest3 = c
        TopRight = x
    if(d>highest4):
        highest4 = d
        TopLeft = x

#Fix orientation of points (ruined previously by transposing)
BottomRight = np.flipud(BottomRight)
BottomLeft = np.flipud(BottomLeft)
TopRight = np.flipud(TopRight)
TopLeft = np.flipud(TopLeft)

#Drawing points
#cv2.circle(img,(BottomRight), 6, (0,0,255), -1)
#cv2.circle(img,(BottomLeft), 6, (0,0,255), -1)
#cv2.circle(img,(TopRight), 6, (0,0,255), -1)
#cv2.circle(img,(TopLeft), 6, (0,0,255), -1)

#Get shape of image
height, width, channels = img.shape 

#Points for perspective transform
pts1= np.float32([TopLeft,TopRight,BottomLeft,BottomRight])
print(pts1)
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
print(pts2)

#Matrix for perspective transform
M = cv2.getPerspectiveTransform(pts1,pts2)

#Get width and height of image for after warp
maxWidth = int(max(np.linalg.norm(BottomLeft-BottomRight),np.linalg.norm(TopLeft-TopRight)))
maxHeight = int(max(np.linalg.norm(TopRight-BottomRight),np.linalg.norm(TopLeft-BottomLeft)))

#Warp image
dst = cv2.warpPerspective(img,M,(maxWidth,maxHeight))

#Plot original + output
plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()

#Show image in new window
#cv2.imshow('dst',dst)
#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()
exit