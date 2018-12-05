# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 20:37:33 2018

@author: ekorz
"""

import cv2
import numpy as np

img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\gridtest.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgblur = cv2.GaussianBlur(imgray, (9, 9), 0);
thresh = cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,5,2)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
dilation = cv2.dilate(thresh, kernel)
imgflip = cv2.bitwise_not(dilation)
edges = cv2.Canny(imgflip,50,150)

lines = cv2.HoughLines(imgflip,1,np.pi/180,100)
for x in range(0, len(lines)):
    for rho,theta in lines[x]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imshow('frame',img)
if cv2.waitKey(1) & 0xFF == ord('q'):
#cam1.release()
    cv2.destroyAllWindows()
    exit()
