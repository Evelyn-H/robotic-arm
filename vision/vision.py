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
        self.cam1 = cv2.VideoCapture(2)
        self.cam1.set(3, 960)
        self.cam1.set(4, 720)
        self.cam2 = cv2.VideoCapture(3)
        self.cam2.set(3, 960)
        self.cam2.set(4, 720)

        self.cut_coords = []
        self.warp_coords = []

        # self.query_image= cv2.imread('image.png',0)
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
        result = self._detectTape(self.get_image_top_camera(), False)
        if result:
            x, y = result
            return x, y
        return None

    # Game

    def is_paper_empty(self):
        img = self.get_image_top_camera()
        black, white, total = self._getBWPixels(img)
        blackPercent = (black * 100) / total
        if blackPercent < 1:
            return True
        return False

    def get_gamegrid(self):
        img = self.get_image_top_camera()
        corners = self._getGridPoints(img)
        # cv2.imshow('frame', img)
        # while not cv2.waitKey(1) & 0xFF == ord('c'):
        # pass
        return corners

    def get_gamestate(self, cross_bound, grid):
        img = self.get_image_top_camera()
        cimg, o = self._detectCircles(img)
        x = self._detectCorners(img, cross_bound)

        if os.environ.get('DEBUG', None):
            def draw(img, corner):
                x, y = tuple(np.uint16(np.around(corner)).ravel())
                if o is not None:
                    for c in o[0]:
                        d = math.sqrt(((int(c[0]) - int(x))**2 + (int(c[1]) - int(y))**2))
                        print('distance', d)
                        # print('d', c[0], x, c[1], y,, (int(c[1]) - int(y))**2, (c[0] - x)**2 + (c[1] - y)**2)
                        if d < 50:
                            return img

                img = cv2.line(img, (x - 20, y - 20), (x + 20, y + 20), (255, 0, 0), 5)
                img = cv2.line(img, (x - 20, y + 20), (x + 20, y - 20), (255, 0, 0), 5)
                # img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
                return img

            for one_x in x:
                draw(cimg, one_x)

            cimg = cv2.line(cimg, (grid[0][0][0], grid[0][0][1]), (grid[0][1][0], grid[0][1][1]), (255, 0, 0), 5)
            cimg = cv2.line(cimg, (grid[1][0][0], grid[1][0][1]), (grid[1][1][0], grid[1][1][1]), (255, 0, 0), 5)
            cimg = cv2.line(cimg, (grid[0][0][0], grid[0][0][1]), (grid[1][0][0], grid[1][0][1]), (255, 0, 0), 5)
            cimg = cv2.line(cimg, (grid[0][1][0], grid[0][1][1]), (grid[1][1][0], grid[1][1][1]), (255, 0, 0), 5)

            cv2.imshow('board state', cimg)
            cv2.waitKey(1)

        return o, x

    def is_hand_in_the_way(self):
        img = self.get_image_top_camera()
        black, white, total = self._getHandPixels(img)
        blackPercent = (black * 100) / (total)
        if blackPercent < 95:
            return True
        return False

    # Private

    def _getImage(self, camera):
        _, frame = camera.read()
        _, frame = camera.read()
        _, frame = camera.read()
        _, frame = camera.read()
        _, frame = camera.read()
        _, frame = camera.read()
        _, frame = camera.read()
        return frame

    def get_image_top_camera(self):
        img = self._getImage(self.cam1)
        corners = np.array(((45, 45), (920, 50), (45, 665), (920, 670)))
        # for x, y in corners:
        # cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        # img = self._warpImage(img, corners)
        x, y, w, h = 60, 70, 840, 590
        img = self._cropImage((x, y, w, h), img)
        # cv2.imshow('frame', img)

        # while not cv2.waitKey(1) & 0xFF == ord('q'):
        #     pass
        return img

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
        # print(pts1)
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        # print(pts2)

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
                    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
                    cv2.imshow('frame', img)
                    # while not cv2.waitKey(1) & 0xFF == ord('q'):
                    #     pass

                return [int(x), int(y), dmm]

            return [int(x), int(y)]
        return []

    # returs rounded numpy array containing circles [x,y,radius]
    def _detectCircles(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgblur = cv2.GaussianBlur(imgray, (9, 9), 0)
        circles = cv2.HoughCircles(imgblur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=35, minRadius=5, maxRadius=30)
        if circles is not None and len(circles) > 0:
            circles = np.uint16(np.around(circles))

        if circles is not None:
            for c in circles[0]:
                cv2.circle(imgblur, (int(c[0]), int(c[1])), c[2], (255, 0, 0), 2)

        if os.environ.get('DEBUG', None):
            cv2.imshow('circles', imgblur)
            cv2.waitKey(1)
        # while not cv2.waitKey(1) & 0xFF == ord('c'):
        # pass
        return imgblur, circles

    def _detectCorners(self, img, cross_bound):
        corners = []

        for x in range(3):
            for y in range(3):
                left = cross_bound[x][y][0]
                top = cross_bound[x][y][1]
                right = cross_bound[x][y][2]
                bottom = cross_bound[x][y][3]

                sub_image = img[top:bottom, left:right]

                imgray = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
                # imgray = cv2.GaussianBlur(imgray, (9, 9), 0)
                # imgray = cv2.medianBlur(imgray, 5)
                _, thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY_INV)
                # thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)
                # thresh = cv2.Canny(imgray, 150, 200)
                count = cv2.countNonZero(thresh)

                if count > 200:
                    corners.append([(left + right) / 2, (top + bottom) / 2])

                if os.environ.get('DEBUG', None):
                    cv2.imshow('corners', thresh)
                    print(count)
                    cv2.waitKey(1)

        return np.array(corners)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # t = int(input("t?"))
        # _, gray = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY_INV)
        # # gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)
        # # img = cv2.medianBlur(img, 5)
        #
        # # gray = np.float32(gray)
        #
        # # Find corners
        # dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        #
        # # result is dilated for marking the corners, not important
        # dst = cv2.dilate(dst, None)
        #
        # # Threshold for an optimal value, it may vary depending on the image.
        # ret, treshH = ret, thresh = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
        #
        # # Get an array with all points
        # points = np.transpose(np.nonzero(treshH))
        #
        # if points is not None:
        #     for p in points:
        #         cv2.circle(gray, (int(p[0]), int(p[1])), 3, (255, 0, 0), 2)
#
        # if os.environ.get('DEBUG', None):
        #     cv2.imshow('corners', gray)
        #     cv2.waitKey(1)
#
        # return points

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
        lines = cv2.HoughLines(imgflip, 1, np.pi / 64, 100)

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

                    if angleDif > 0.8:
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

                        cv2.line(img, (x1_1, y1_1), (x1_2, y1_2), (0, 0, 255), 2)
                        cv2.line(img, (x2_1, y2_1), (x2_2, y2_2), (0, 0, 255), 2)
                        cv2.circle(img, (int(x), int(y)), 3, (255, 0, 0), 1, 8, 0)

        for index, x in enumerate(corners):
            remove = []
            for index2, x2 in enumerate(corners):
                if index != index2:
                    distance = math.sqrt(((x[0] - x2[0])**2 + (x[1] - x2[1])**2))
                    if distance < 10:
                        remove.append(index2)
            remove.sort(reverse=True)
            for x3 in remove:
                del corners[x3]

        if os.environ.get('DEBUG', None):
            cv2.imshow('gridpoints', img)
            cv2.waitKey(1)

        return corners

    def _getBWPixels(self, img):
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 140, 255, 0)
        kernel = np.ones((7, 7), np.uint8)
        thresh2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        height, width = thresh2.shape
        white = cv2.countNonZero(thresh2)
        black = (height * width) - white
        return black, white, height * width

    def _getHandPixels(self, img):
        #convert image
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

        #get bounds for skin color
        smin = np.array((0, 133, 77))
        smax = np.array((255, 173, 127))

        #find skin
        mask = cv2.inRange(ycrcb, smin, smax)

        kernel = np.ones((7, 7), np.uint8)
        opens = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        height, width = opens.shape
        white = cv2.countNonZero(opens)
        black = (height * width) - white

        if os.environ.get('DEBUG', None):
            opens = cv2.cvtColor(opens, cv2.COLOR_GRAY2RGB)
            opens[:, :, 1] = np.zeros((opens.shape[0], opens.shape[1]), dtype=np.float32)
            opens = cv2.add(opens, img)
            cv2.imshow('hand', opens)
            cv2.waitKey(1)

        return black, white, height * width

    def _detectFeatures(self, query_img, train_img):
        MIN_MATCH_COUNT = 5
        # Initiate SIFT detector
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(query_img, None)
        des1 = np.float32(des1)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)
        img2 = cv2.cvtColor(train_img, cv2.COLOR_BGR2GRAY)

        # img2 = cv2.imread('vlcsnap-2018-12-04-13h43m11s468.png',0) # trainImage

        # find the keypoints and descriptors with SIFT
        kp2, des2 = orb.detectAndCompute(img2, None)
        des2 = np.float32(des2)

        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            return M, mask
        else:
            print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
            return
