# -*- coding: utf-8 -*-

import cv2
import numpy as np

#load image
img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\f1.png')
img2 = cv2.GaussianBlur(img,(5,5),1.4)
#convert to HSV
hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

#define range of red color
redLower1 = np.array([0, 70, 50])
redUpper1 = np.array([10, 255, 255])

#Red is in 0-10 and 160-180, so we need 2 bounds
redLower2 = np.array([160, 70, 50])
redUpper2 = np.array([180, 255, 255])

#Make masks
mask1 = cv2.inRange(hsv, redLower1, redUpper1)
mask2 = cv2.inRange(hsv, redLower2, redUpper2)

#Combine masks
mask = mask1 | mask2

#Erode some stuff
kernel = np.ones((7,7),np.uint8)
eroded = cv2.erode(mask,kernel,1)

#Get contour of what's left
im2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Get moments and using that, a center point of the countour
M = cv2.moments(contours[0])
x = M["m10"] / M["m00"];   
y = M["m01"] / M["m00"];

#Draw stuff
#cv2.circle(img, (int(x), int(y)), 7, (255, 255, 255), -1)
#cv2.drawContours(img, contours, -1, (127,255,255), 3)

#Show stuff
#cv2.imshow('Mask',img)
#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()
exit