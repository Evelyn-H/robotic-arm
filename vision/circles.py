# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:42:10 2019

@author: ekorz
"""
import cv2
import numpy as np


corners = np.array(((45, 45), (920, 50), (920, 670), (45, 665)))
page_mask = np.zeros((720, 960), dtype=np.uint8)
page_mask = cv2.fillConvexPoly(page_mask, corners, (255, 255, 255))

def mask_background(img):
    return cv2.bitwise_and(img, img, mask=page_mask)


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
        for i in circles[0, :]:
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(image, (i[0], i[1]), 1, (0, 0, 255), 2)
    return image

def threshold_image(img):
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
    lower = np.array([40, 65, 40])
    upper = np.array([80, 255, 255])
    greenmask = cv2.inRange(hsv, lower, upper)

    #mask for blue
    lower = np.array([100, 80, 70])
    upper = np.array([140, 255, 255])
    bluemask = cv2.inRange(hsv, lower, upper)

    #blur
    redblur = cv2.medianBlur(redmask, 11)
    greenblur = cv2.medianBlur(greenmask, 11)
    blueblur = cv2.medianBlur(bluemask, 11)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
    redblur = cv2.morphologyEx(redblur, cv2.MORPH_OPEN, kernel)
    greenblur = cv2.morphologyEx(greenblur, cv2.MORPH_OPEN, kernel)
    blueblur = cv2.morphologyEx(blueblur, cv2.MORPH_OPEN, kernel)

    redblur = cv2.GaussianBlur(redblur, (5, 5), 1.4)
    greenblur = cv2.GaussianBlur(greenblur, (5, 5), 1.4)
    blueblur = cv2.GaussianBlur(blueblur, (5, 5), 1.4)

    return redblur, greenblur, blueblur

def detect_circles(img):
    # return cv2.HoughCircles(redblur,   cv2.HOUGH_GRADIENT, 1, 10, param1=100, param2=20, minRadius=0, maxRadius=0)
    return find_centers(img)

def process_and_get_avg_centers(img, render=False):
    img = mask_background(img)
    redblur, greenblur, blueblur = threshold_image(img)

    superimposed = np.zeros((redblur.shape[0], redblur.shape[1], 3), dtype=np.float32)
    superimposed[:, :, 0] = blueblur / 255.0
    superimposed[:, :, 1] = greenblur / 255.0
    superimposed[:, :, 2] = redblur / 255.0

    def avg_circles(circles):
        if circles is None or not len(circles[0]) == 4:
            return None
        return np.reshape(np.mean(circles, axis=1), (1, 1, 3))

    redcircles = detect_circles(redblur)
    greencircles = detect_circles(greenblur)
    bluecircles = detect_circles(blueblur)

    redcenter = avg_circles(redcircles)
    greencenter = avg_circles(greencircles)
    bluecenter = avg_circles(bluecircles)

    if redcenter is None or greencenter is None or bluecenter is None:
        return img, None, None, None

    if render:
        img = draw_circles(img, redcenter)
        img = draw_circles(img, greencenter)
        img = draw_circles(img, bluecenter)

        #add and draw circles for testing
        img = draw_circles(img, redcircles)
        img = draw_circles(img, greencircles)
        img = draw_circles(img, bluecircles)

    return img, redcenter[0][0][0:2], greencenter[0][0][0:2], bluecenter[0][0][0:2]


if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    cam.set(3, 960); cam.set(4, 720)

    while True:

        # read image from camera feed
        _, img = cam.read()

        img, redcenter, greencenter, bluecenter = process_and_get_avg_centers(img, render=True)

        cv2.imshow('image', img)
        # cv2.imshow('image',superimposed)
        cv2.waitKey(1)

    cv2.destroyAllWindows()
