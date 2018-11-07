# -*- coding: utf-8 -*-
import cv2
import numpy as np
import numpy.linalg as la

class Vision(object):
    """docstring for Vision."""

    def __init__(self):
        # start video capture
        self.cam1 = cv2.VideoCapture(0)
        self.cam2 = cv2.VideoCapture(1)

        self.cut_coords = []


    # Control

    def get_pen_height(self):
        ...

    def get_pen_pos(self):
        ...

    # Game

    def is_paper_empty(self):
        ...

    def get_gamestate():
        '''tic tac toe'''
        ...

    def is_hand_in_the_way():
        ...

    # Private

    def _getImage(self, camera):
        ret, frame = camera.read()
        return frame

    def _cutCoords(self, image):

        #turn it into grayscale
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #threshold
        ret2, thresh = cv2.threshold(imgray, 120, 255, 0)

        #create kernel for noise removal
        kernel = np.ones((7,7),np.uint8)

        #erosion then dilation
        thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        #find all contours and get the largest
        (_,contours,_) = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        largest = 0
        largestContour = 0
        for contour in contours:
            a = cv2.contourArea(contour)
            if(a>largest):
                largest = a
                largestContour = contour

        #get bounding rectangle of largest contour
        x,y,w,h = cv2.boundingRect(largestContour)

        return [x,y,w,h]

    def _cropImage(self, coords, image):
        #crop image around largest contour
        x,y,w,h = coords
        return image[y:y+h, x:x+w]

    def _warpImage(self, img):
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
        #cv2.circle(img,(BottomRight[0],BottomRight[1]), 6, (0,0,255), -1)
        #cv2.circle(img,(BottomLeft[0],BottomLeft[1]), 6, (0,0,255), -1)
        #cv2.circle(img,(TopRight[0],TopRight[1]), 6, (0,0,255), -1)
        #cv2.circle(img,(TopLeft[0],TopLeft[1]), 6, (0,0,255), -1)

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
        return dst

    #returns [x,y] of center of blue tape and height of the center if frontCamera is true
    def _detectTape(self, img, frontCamera):
        lower = np.array([100, 120, 30])
        upper = np.array([140, 255, 255])
        img2 = cv2.GaussianBlur(img,(5,5),1.4)
        hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((7,7),np.uint8)
        eroded = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        im2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if contours:
            M = cv2.moments(contours[0])
            x = M["m10"] / M["m00"];
            y = M["m01"] / M["m00"];
            if frontCamera:
                rect = cv2.minAreaRect(contours[0])
                height = max([rect[1][0],rect[1][1]])
                #Where paper begins on left
                xleft = 0
                yleft = 521

                #Where paper begins on right
                xright = 960
                yright = 531
                #Create points
                p1 = [xleft,yleft]
                p2 = [xright,yright]
                p3 = [int(x),int(y)]

                #Calculate distance
                d = la.norm(np.cross(np.array(p2)-np.array(p1), np.array(p1)-np.array(p3)))/la.norm(np.array(p2)-np.array(p1))

                #Since height of rectangle is 2.6cm, get distance in mm
                dmm = (23 * d) / height
                return [int(x), int(y), dmm]

        return [int(x), int(y)]

    #returs rounded numpy array containing circles [x,y,radius]
    def _detectCircles(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgblur = cv2.GaussianBlur( imgray,(9, 9), 0);
        circles = cv2.HoughCircles(imgblur,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
        if circles is not None and len(circles) > 0:
            circles = np.uint16(np.around(circles))
        return circles
