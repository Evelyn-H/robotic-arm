# -*- coding: utf-8 -*-

import cv2
import numpy as np
import numpy.linalg as la

cap = cv2.VideoCapture(0)
lower = np.array([100, 120, 30])
upper = np.array([140, 255, 255])

#load image
#img = cv2.imread('C:\\Users\\ekorz\\Desktop\\Project\\Images\\fb3.png')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    img2 = cv2.GaussianBlur(frame,(5,5),1.4)
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    kernel = np.ones((7,7),np.uint8)
    eroded = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    im2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if contours:
        rect = cv2.minAreaRect(contours[0])
        height = max([rect[1][0],rect[1][1]])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(frame,[box],0,(0,0,255),2)
        height = max([rect[1][0],rect[1][1]])
        M = cv2.moments(contours[0])
        x = M["m10"] / M["m00"];   
        y = M["m01"] / M["m00"];
        cv2.circle(frame, (int(x), int(y)), 7, (255, 255, 255), -1)

   
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Draw stuff
#cv2.circle(img, (int(x), int(y)), 7, (255, 255, 255), -1)
#cv2.drawContours(img, contours, -1, (127,255,255), 3)

#Show stuff
#cv2.imshow('Mask',img)
#if cv2.waitKey(0) & 0xff == 27:
#    cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()
exit