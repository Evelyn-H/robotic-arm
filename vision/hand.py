# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 23:02:01 2019

@author: ekorz
"""

import cv2
import numpy as np


cam1 = cv2.VideoCapture(3)
cam1.set(3, 960)
cam1.set(4, 720)

while(True):
    _, im = cam1.read()
    im_ycrcb = cv2.cvtColor(im, cv2.COLOR_BGR2YCR_CB)

    skin_ycrcb_mint = np.array((0, 133, 77))
    skin_ycrcb_maxt = np.array((255, 173, 127))
    skin_ycrcb = cv2.inRange(im_ycrcb, skin_ycrcb_mint, skin_ycrcb_maxt)

    kernel = np.ones((7,7),np.uint8)
    opens = cv2.morphologyEx(skin_ycrcb, cv2.MORPH_OPEN, kernel)
    height, width = opens.shape
    white = cv2.countNonZero(opens);
    black = (height*width)-white;
    blackPercent = (black*100)/(height*width)
    print(blackPercent)
    if blackPercent < 95:
        handintheway = True


    cv2.imshow('dst',opens)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cam1.release()
cv2.destroyAllWindows()
