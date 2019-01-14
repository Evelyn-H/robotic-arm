# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:42:10 2019

@author: ekorz
"""
import cv2
import numpy as np


cam = cv2.VideoCapture(0)
cam.set(3, 960); cam.set(4, 720)


def find_centers(image):
    im2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    for c in contours:
        # calculate moments for each contour
        # M = cv2.moments(c)
        # # calculate x,y coordinate of center
        # x = int(M["m10"] / M["m00"])
        # y = int(M["m01"] / M["m00"])
        # cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

        (x, y), radius = cv2.minEnclosingCircle(c)

        centers.append([x, y, radius])

    return np.array([centers])


def draw_circles(image, circles):
    # print(circles)
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
    return image

while True:

    # read image from camera feed
    _, img = cam.read()

    #convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #mask for red
    lower = np.array([0, 100, 100])
    upper = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)

    lower = np.array([160, 100, 100])
    upper = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower, upper)

    #combine red masks
    redmask = cv2.add(mask, mask2)

    #mask for green
    lower = np.array([40, 65, 65])
    upper = np.array([80, 255, 255])
    greenmask = cv2.inRange(hsv, lower, upper)

    #mask for blue
    lower = np.array([100, 60, 45])
    upper = np.array([140, 255, 255])
    bluemask = cv2.inRange(hsv, lower, upper)


    #blur

    redblur = cv2.medianBlur(redmask, 5)
    greenblur = cv2.medianBlur(greenmask, 5)
    blueblur = cv2.medianBlur(bluemask, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
    redblur = cv2.morphologyEx(redblur, cv2.MORPH_OPEN, kernel)
    greenblur = cv2.morphologyEx(greenblur, cv2.MORPH_OPEN, kernel)
    blueblur = cv2.morphologyEx(blueblur, cv2.MORPH_OPEN, kernel)

    # redblur = cv2.GaussianBlur(redblur, (5, 5), 1.4)
    # greenblur = cv2.GaussianBlur(greenblur, (5, 5), 1.4)
    # blueblur = cv2.GaussianBlur(blueblur, (5, 5), 1.4)

    superimposed = np.zeros((redblur.shape[0], redblur.shape[1], 3), dtype=np.float32)
    superimposed[:, :, 0] = blueblur
    superimposed[:, :, 1] = greenblur
    superimposed[:, :, 2] = redblur

    # c = cv2.findContours(blueblur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(c)
    # M = cv2.moments(redblur)
    # cX = int(M["m10"] / M["m00"])
    # cY = int(M["m01"] / M["m00"])
    # print(cX)
    # print(cY)

    #detect circles
    # redcircles   = cv2.HoughCircles(redblur,   cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=20, minRadius=0, maxRadius=0)
    # greencircles = cv2.HoughCircles(greenblur, cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=20, minRadius=0, maxRadius=0)
    # bluecircles  = cv2.HoughCircles(blueblur,  cv2.HOUGH_GRADIENT, 1, 10, param1=50, param2=20, minRadius=0, maxRadius=0)

    redcircles = find_centers(redblur)
    greencircles = find_centers(greenblur)
    bluecircles = find_centers(blueblur)

    # print("red:", redcircles)
    # print("green:", greencircles)
    # print("blue:", bluecircles)

    #add and draw circles for testing
    # rb = np.append(redcircles,greencircles,axis=1)
    # circles = np.append(rb,bluecircles,axis=1)
    img = draw_circles(img, redcircles)
    img = draw_circles(img, greencircles)
    img = draw_circles(img, bluecircles)

    cv2.imshow('image', img)
    # cv2.imshow('image',superimposed)
    cv2.waitKey(1)

cv2.destroyAllWindows()
