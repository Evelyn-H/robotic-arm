# -*- coding: utf-8 -*-
import os
import itertools
import math

import cv2
import numpy as np
import numpy.linalg as la


class Vision(object):
    """docstring for Vision."""

    def __init__(self):
        # start video capture
        self.cam1 = cv2.VideoCapture(0)
        self.cam1.set(3, 960)
        self.cam1.set(4, 720)
        self.cam2 = cv2.VideoCapture(1)
        self.cam2.set(3, 960)
        self.cam2.set(4, 720)

        self.cut_coords = []
        self.warp_coords = []

        self.query_image= cv2.imread('image.png',0)
    # Control

    def get_pen_height(self):
        i = self._getImage(self.cam2)
        # cv2.imshow('frame', i)
        # while not cv2.waitKey(1) & 0xFF == ord('q'):
            # pass
        result = self._detectTape(i, True)
        if result:
            x, y, h = result
            return h
        return None

    def get_pen_pos(self):
        result = self._detectTape(self._getImage(self.cam1), False)
        if result:
            x, y = result
            return x, y
        return None

    # Game

    def is_paper_empty(self):
        img = self._getImage(self.cam1)
        cutImg = self._cropImage(self.cut_coords, img)
        warpImg = self._warpImage(self.warp_coords, cutImg)
        black, white, total = self._getBWPixels(self, warpImg)
        blackPercent = (black * 100) / total
        if blackPercent < 1:
            return True
        return False

    def get_gamegrid(self):
        img = self._getImage(self.cam1)
        cutImg = self._cropImage(self.cut_coords, img)
        warpImg = self._warpImage(self.warp_coords, cutImg)
        self._getGridPoints(self, warpImg)

    def get_gamestate(self):
        img = self._getImage(self.cam1)
        cutImg = self._cropImage(self.cut_coords, img)
        warpImg = self._warpImage(self.warp_coords, cutImg)
        return self._detectCircles(warpImg), self._detectCorners(self, warpImg)

    def is_hand_in_the_way(self):
        img = self._getImage(self.cam1)
        cutImg = self._cropImage(self.cut_coords, img)
        warpImg = self._warpImage(self.warp_coords, cutImg)
        black, white, total = self._getBWPixels(self, warpImg)
        blackPercent = (black*100)/(total)
        if blackPercent < 95:
            return True
        return False

    # Private

    def _getImage(self, camera):
        _, frame = camera.read()
        return frame

    def _cutCoords(self, image):

        # turn it into grayscale
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # threshold
        ret2, thresh = cv2.threshold(imgray, 120, 255, 0)

        # create kernel for noise removal
        kernel = np.ones((7, 7), np.uint8)

        # erosion then dilation
        thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # find all contours and get the largest
        (_, contours, _) = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        largest = 0
        largestContour = 0
        for contour in contours:
            a = cv2.contourArea(contour)
            if a > largest:
                largest = a
                largestContour = contour

        # get bounding rectangle of largest contour
        x, y, w, h = cv2.boundingRect(largestContour)

        return [x, y, w, h]

    def _cropImage(self, coords, image):
        # crop image around largest contour
        x, y, w, h = coords
        return image[y:y + h, x:x + w]

    def _warpCoords(self, img):
        # Turn into grayscale
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Threshold
        ret, thresh = cv2.threshold(imgray, 140, 255, 0)

        # Kernel for noise filtering
        kernel = np.ones((7, 7), np.uint8)

        # Noise filtering
        # thresh2 = cv2.erode(thresh,kernel,1)
        thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Find corners
        dst = cv2.cornerHarris(thresh2, 2, 3, 0.04)

        # result is dilated for marking the corners, not important
        dst = cv2.dilate(dst, None)

        # Threshold for an optimal value, it may vary depending on the image.
        ret, treshH = ret, thresh = cv2.threshold(dst, 0, 255, 0)

        # Get an array with all points
        points = np.transpose(np.nonzero(treshH))

        # Find corners closest to edges
        highest1 = -10000
        highest2 = -10000
        highest3 = -10000
        highest4 = -10000

        for x in points:
            a = x[0] + x[1]
            b = x[0] - x[1]
            c = x[1] - x[0]
            d = -x[0] - x[1]
            if a > highest1:
                highest1 = a
                BottomRight = x
            if b > highest2:
                highest2 = b
                BottomLeft = x
            if c > highest3:
                highest3 = c
                TopRight = x
            if d > highest4:
                highest4 = d
                TopLeft = x

        # Fix orientation of points (ruined previously by transposing)
        BottomRight = np.flipud(BottomRight)
        BottomLeft = np.flipud(BottomLeft)
        TopRight = np.flipud(TopRight)
        TopLeft = np.flipud(TopLeft)
        return TopLeft, TopRight, BottomLeft, BottomRight

    def _warpImage(self, img, warpCoords):

        TopLeft, TopRight, BottomLeft, BottomRight = warpCoords

        # Drawing points
        # cv2.circle(img,(BottomRight[0],BottomRight[1]), 6, (0,0,255), -1)
        # cv2.circle(img,(BottomLeft[0],BottomLeft[1]), 6, (0,0,255), -1)
        # cv2.circle(img,(TopRight[0],TopRight[1]), 6, (0,0,255), -1)
        # cv2.circle(img,(TopLeft[0],TopLeft[1]), 6, (0,0,255), -1)

        # Get shape of image
        height, width, channels = img.shape

        # Points for perspective transform
        pts1 = np.float32([TopLeft, TopRight, BottomLeft, BottomRight])
        print(pts1)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        print(pts2)

        # Matrix for perspective transform
        M = cv2.getPerspectiveTransform(pts1, pts2)

        # Get width and height of image for after warp
        maxWidth = int(max(np.linalg.norm(BottomLeft - BottomRight), np.linalg.norm(TopLeft - TopRight)))
        maxHeight = int(max(np.linalg.norm(TopRight - BottomRight), np.linalg.norm(TopLeft - BottomLeft)))

        # Warp image
        dst = cv2.warpPerspective(img, M, (maxWidth, maxHeight))
        return dst

    # returns [x,y] of center of blue tape and height of the center if frontCamera is true
    def _detectTape(self, img, frontCamera, paper_left=(0, 490), paper_right=(959, 500), tape_height=7, tape_offset=7):
        img2 = cv2.GaussianBlur(img, (5, 5), 1.4)
        hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        lower = np.array([160, 100, 100])
        upper = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower, upper)

        mask = cv2.add(mask, mask2)

        kernel = np.ones((7, 7), np.uint8)
        eroded = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        im2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if contours:
            M = cv2.moments(contours[0])
            x = M["m10"] / M["m00"]
            y = M["m01"] / M["m00"]
            if frontCamera:
                rect = cv2.minAreaRect(contours[0])
                height = max([rect[1][0], rect[1][1]])

                # Create points
                p1 = paper_left
                p2 = paper_right
                p3 = [int(x), int(y)]

                # Calculate distance
                d = la.norm(np.cross(np.array(p2) - np.array(p1), np.array(p1) - np.array(p3))) / la.norm(np.array(p2) - np.array(p1))

                # Since height of rectangle is 2.6cm, get distance in mm
                dmm = (tape_height * d) / height
                # tip of pen instead of middle of tape
                dmm = dmm - tape_offset - tape_height / 2

                if os.environ.get('DEBUG', None):
                    cv2.circle(img, paper_left, 5, (0, 0, 255), -1)
                    cv2.circle(img, paper_right, 5, (0, 0, 255), -1)
                    cv2.drawContours(img, contours, -1, (0,255,0), 3)
                    cv2.imshow('frame', img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()

                return [int(x), int(y), dmm]

            return [int(x), int(y)]
        return []

    # returs rounded numpy array containing circles [x,y,radius]
    def _detectCircles(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgblur = cv2.GaussianBlur(imgray, (9, 9), 0)
        circles = cv2.HoughCircles(imgblur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=30)
        if circles is not None and len(circles) > 0:
            circles = np.uint16(np.around(circles))
        return circles
    
    def _detectCorners(self, img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        gray = np.float32(gray)
        
        # Find corners
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        
        # result is dilated for marking the corners, not important
        dst = cv2.dilate(dst, None)
        
        # Threshold for an optimal value, it may vary depending on the image.
        ret, treshH = ret, thresh = cv2.threshold(dst, 0.1*dst.max(), 255, 0)
        
        # Get an array with all points
        points = np.transpose(np.nonzero(treshH))
        
        return points

# =============================================================================
#     def _detectLines(self, img):
#         imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         imgblur = cv2.GaussianBlur(imgray, (9, 9), 0);
#         thresh = cv2.adaptiveThreshold(imgblur,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,5,2)
#         kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
#         dilation = cv2.dilate(thresh, kernel)
#         imgflip = cv2.bitwise_not(dilation)
#         lines = cv2.HoughLines(imgflip,1,np.pi/180,100)
#         return lines
# =============================================================================

    def _getGridPoints(self, img):
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

    def _getBWPixels(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 140, 255, 0)
        kernel = np.ones((7,7),np.uint8)
        thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        height, width = thresh2.shape
        white = cv2.countNonZero(thresh2);
        black = (height*width)-white;
        return black, white, height*width

    def _getHandPixels(self, img):
        #convert image
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)     
        
        #get bounds for skin color
        smin = np.array((0, 133, 77))
        smax = np.array((255, 173, 127))
        
        #find skin
        mask = cv2.inRange(ycrcb, smin, smax)
    
        kernel = np.ones((7,7),np.uint8)
        opens = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        height, width = opens.shape
        white = cv2.countNonZero(opens);
        black = (height*width)-white;
        return black, white, height*width

    def _detectFeatures(self, query_img, train_img):
        MIN_MATCH_COUNT = 5
        # Initiate SIFT detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(query_img, None)
        des1 = np.float32(des1)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        img2 = cv2.cvtColor(train_img, cv2.COLOR_BGR2GRAY)

        # img2 = cv2.imread('vlcsnap-2018-12-04-13h43m11s468.png',0) # trainImage

        # find the keypoints and descriptors with SIFT
        kp2, des2 = orb.detectAndCompute(img2,None)
        des2 = np.float32(des2)

        matches = flann.knnMatch(des1,des2,k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)


        if len(good)>MIN_MATCH_COUNT:
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
            return M, mask
        else:
            print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
            return