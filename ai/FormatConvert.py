# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 09:11:24 2018

@author: heier
"""

import numpy as np
import cv2

class FormatConvert:

#    def drawFromFile(arm):
#        f = open("currentDrawing.txt", 'r')
#        armUp = False
#        for line in f:
#            if line == "NEWLINE\n":
#                arm.up()
#                armUp = True
#            else:
#                x, y = line.split()
#                arm.move_to([float(y), float(x)], speed=1)
#
#            if (armUp):
#                arm.down()
#                armUp = False
#
#        f.close()

    # Draws a drawing from a text file. Allows for scaling and
    # shifting of what is drawn.
    @classmethod
    def drawFromFile(cls, file, arm, scale1=None, shift1=None, speed=1):
        pl = cls.pointsToAr(file)
        # for l in pl:
            # print(l)
        pl = cls.scaleShift(pl, scale=scale1, shift=shift1)
        # print()
        # for l in pl:
            # print(l)
        for line in pl:
            arm.up()
            arm.move_to([float(line[0][1]), float(line[0][0])], speed=speed)
            arm.down()
            for p in line:
                arm.move_to([float(p[1]), float(p[0])], speed=speed)
            arm.up()

        arm.up()


    # Scale cm values of drawing.
    @staticmethod
    def scaleShift(pl, scale=None, shift=None):
        newPl = []

        for l in pl:
            newPl.append([])
            for p in l:
                x, y = p[0], p[1]
                #first, scale
                if not scale == None:
                    x = scale[1]*x
                    y = scale[0]*y

                # Then shift
                if not shift == None:
                    x += shift[1]
                    y += shift[0]

                newPl[len(newPl)-1].append((x,y))

        return newPl


    @staticmethod
    def pointsToAr(file):
        f = open(file, 'r')
        ls = []
        for line in f:
            if line == "NEWLINE\n":
                ls.append([])
            else:
                x, y = line.split()
                x = float(x)
                y = float(y)
                ls[len(ls)-1].append((x,y))
        f.close()
        return ls

    @staticmethod
    def convertToPixelCoordinates(pl, scale, offset):
        newPl = []
        for l in pl:
            newPl.append([])
            for p in l:
                newPl[len(newPl)-1].append(
                        FormatConvert.singlePointConvert(p, scale, offset))

        return newPl

    # Converts coordinate system from centimeters
    # To pixel values.
    # Standard scale is 10 pixels per cm
    @staticmethod
    def singlePointConvert(p, scale, offset):
        # First, shift (0,0) to upper left corner
        newX = scale[1]*(p[0]+(42.0/2))
        newY = scale[0]*(p[1]+(29.7/2))

        # Convert to pixel value
        newX = int((newX*10) + offset[1])
        newY = int((newY*10) + offset[0])

        return (newX, newY)

    @staticmethod
    def findExtrema(pl, imgx, imgy):
        xMin, yMin = imgx, imgy
        xMax, yMax = 0, 0

        for l in pl:
            for p in l:
                if (xMin > p[1]):
                    xMin = p[1]
                if (yMin > p[0]):
                    yMin = p[0]
                if (xMax < p[1]):
                    xMax = p[1]
                if (yMax < p[0]):
                    yMax = p[0]

        return xMin, yMin, xMax, yMax


#    def convertPoint(x, y):
#        global bgoffsetx, bgoffsety, bgx, bgy
#        newX = x-(bgoffsetx + bgx/2)
#        newY = y-(bgoffsety + bgy/2)
#
#        newX = a3xcm*(float(newX)/float(bgx))
#        newY = a3ycm*(float(newY)/float(bgy))
#
#        return (newX, newY)

    # Takes file that is a list of points, and
    # converts them into a numpy 2d uint8 array
    # drawing.
    # The standard format is 297x420 image.
    # Be aware: First coordinate is height,
    # second coordinate is width.

    #   Scale: change img to other dimensions.
    #   offset: Offset img in pixels.
    #   Window: Only return part of the img.
    #   borderWindow: Takes a window centered on
    #       image by finding the extreme coordinates
    #       and adding a specified pixel border.
    #       This overrides the window.
    @staticmethod
    def filePointToImg(file,
                    scale=(1.0, 1.0),
                    offset=(0,0),
                    window=None,
                    borderWindow=None,
                    lineWidth=2,
                    pl=None):
        imgy = int(297.0*scale[0])
        imgx = int(420.0*scale[1])

        # Only bother with file if there is not a point list given.
        if pl==None:
            # Get a list of lines to the right coordinate types.
            # First put the points into array
            pl = FormatConvert.pointsToAr(file)
        # Then format to appropriate type
        pl = FormatConvert.convertToPixelCoordinates(pl, scale, offset)
        print(pl)

        # Create image.
        img = np.zeros((imgy, imgx), dtype=np.uint8)
        # for each line
        for i in range(len(pl)):
            # draw each line segment
            for j in range(len(pl[i])-1):
                cv2.line(img, pl[i][j], pl[i][j+1],
                         (255,255,255), lineWidth)

        if not borderWindow==None:
            # Be aware: I flipped the coordinates at some point,
            # But don't care about that rn.
            x1, y1, x2, y2 = FormatConvert.findExtrema(pl, imgx, imgy)

            if isinstance(borderWindow, int):
                x1 -= borderWindow
                x2 += borderWindow
                y1 -= borderWindow
                y2 += borderWindow

            elif len(borderWindow)==2:
                x1 -= borderWindow[0]
                x2 += borderWindow[0]
                y1 -= borderWindow[1]
                y2 += borderWindow[1]

            elif len(borderWindow)==4:
                x1 -= borderWindow[0]
                x2 += borderWindow[2]
                y1 -= borderWindow[1]
                y2 += borderWindow[3]

            # Ensure no out-of-bounds error happens
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(imgy, x2)
            y2 = min(imgx, y2)

            img2 = img[x1:x2, y1:y2]
            img = img2

        else: # BorderWindow overrules window
            if not window==None:
                x1, y1, x2, y2 = window
                img2 = img[x1:x2, y1:y2]
                img = img2

        return img

gridFile = "ai/game/TTTLines.txt"
circleFile = "ai/game/TTTCircle.txt"
crossFile = "ai/game/TTTCross.txt"
