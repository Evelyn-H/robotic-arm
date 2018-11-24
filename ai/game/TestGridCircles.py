
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 13:41:46 2018
 
@author: ekorz
"""
import cv2
import numpy as np
import itertools
import math
 
img = cv2.imread('yourimagehere.jpg')
 
def _getGridPoints(img):
    def perp(a):
        b = np.empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b
    height, width, channels = img.shape
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(imgblur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilation = cv2.dilate(thresh, kernel)
    imgflip = cv2.bitwise_not(dilation)
    lines = cv2.HoughLines(imgflip, 1, np.pi / 180, 100)
 
    corners = []
 
    for rho, theta in itertools.chain(*lines):
        for rho2, theta2 in itertools.chain(*lines):
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1_1 = int(x0 + 1000 * (-b))
                y1_1 = int(y0 + 1000 * (a))
                x1_2 = int(x0 - 1000 * (-b))
                y1_2 = int(y0 - 1000 * (a))
 
                a = np.cos(theta2)
                b = np.sin(theta2)
                x0 = a * rho2
                y0 = b * rho2
                x2_1 = int(x0 + 1000 * (-b))
                y2_1 = int(y0 + 1000 * (a))
                x2_2 = int(x0 - 1000 * (-b))
                y2_2 = int(y0 - 1000 * (a))
 
                angleDif = abs(theta - theta2)
 
                if angleDif > 0.1:
                    a1 = np.array([x1_1, y1_1])
                    a2 = np.array([x1_2, y1_2])
                    b1 = np.array([x2_1, y2_1])
                    b2 = np.array([x2_2, y2_2])
                    da = a2 - a1
                    db = b2 - b1
                    dp = a1 - b1
                    dap = perp(da)
                    denom = np.dot(dap, db)
                    num = np.dot(dap, dp)
                    x, y = (num / denom.astype(float)) * db + b1
 
                    if int(x) < width and int(x) > 0 and int(y) < height and int(y) > 0:
                        corners.append([int(x), int(y)])
                       
                        #cv2.circle(img, (int(x), int(y)), 3, (255, 0, 0), 1, 8, 0)
        for index, x in enumerate(corners):
            remove = []
            for index2, x2 in enumerate(corners):
                if index != index2:
                    distance = math.sqrt(((x[0]-x2[0])**2 + (x[1]-x2[1])**2))
                    if distance < 5:
                        remove.append(index2)
            remove.sort(reverse=True)
            for x3 in remove:
                del corners[x3]
        return corners
   
def _detectCircles(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgray, (9, 9), 0)
    circles = cv2.HoughCircles(imgblur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))
    return circles