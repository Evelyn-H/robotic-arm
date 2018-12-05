# -*- coding: utf-8 -*-

import cv2
import numpy as np
import numpy.linalg as la

#load image
img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\fb3.png')
img2 = cv2.GaussianBlur(img,(5,5),1.4)
#convert to HSV
hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

#define range of red color
#redLower1 = np.array([0, 70, 50])
#redUpper1 = np.array([10, 255, 255])

#Blue is in 100-140, so we need 2 bounds
lower = np.array([100, 120, 30])
upper = np.array([140, 255, 255])

#Make mask
mask = cv2.inRange(hsv, lower, upper)

#Erode some stuff
kernel = np.ones((7,7),np.uint8)
eroded = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)


#Get contour of what's left
im2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#Get bounding rectangle of contour
rect = cv2.minAreaRect(contours[0])
#box = cv2.boxPoints(rect)
#box = np.int0(box)
#cv2.drawContours(img,[box],0,(0,0,255),2)

#Get height of rectangle
height = max([rect[1][0],rect[1][1]])

#Get moments and using that, a center point of the countour
M = cv2.moments(contours[0])
x = M["m10"] / M["m00"];   
y = M["m01"] / M["m00"];

#Where paper begins on left
xleft = 0
yleft = 521

#Where paper begins on right
xright = 960
yright= 531

#Create points
p1 = [xleft,yleft]
p2 = [xright,yright]
p3 = [int(x),int(y)]

#Calculate distance
d = la.norm(np.cross(np.array(p2)-np.array(p1), np.array(p1)-np.array(p3)))/la.norm(np.array(p2)-np.array(p1))

#Since height of rectangle is 2.6cm, get distance in mm
dmm = (23 * d) / height

#Draw stuff
#cv2.circle(img, (int(x), int(y)), 7, (255, 255, 255), -1)
#cv2.drawContours(img, contours, -1, (127,255,255), 3)

#Show stuff
#cv2.imshow('Mask',img)
#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()
exit