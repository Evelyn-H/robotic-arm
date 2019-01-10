import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import deque

MIN_MATCH_COUNT = 5
img1 = cv2.imread('images/qrblur.png',0)          # queryImage
# Initiate SIFT detector
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1,None)
# des1 = np.float32(des1)

# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# search_params = dict(checks = 50)

# matcher = cv2.FlannBasedMatcher(index_params, search_params)
matcher = cv2.BFMatcher(cv2.NORM_HAMMING)


cam = cv2.VideoCapture(0)
cam.set(3, 960); cam.set(4, 720)

avg_len = 5
avg_buffer = deque(maxlen=avg_len)

while True:
    _, frame = cam.read()

    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # img2 = cv2.imread('vlcsnap-2018-12-04-13h43m11s468.png',0) # trainImage

    # find the keypoints and descriptors with SIFT
    kp2, des2 = orb.detectAndCompute(img2,None)
    # des2 = np.float32(des2)

    matches = matcher.knnMatch(des1,des2,k=2)
    # matches = matcher.match(des1,des2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    matches = good


    if len(matches)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        if not M is None:
            dst = cv2.perspectiveTransform(pts,M)

            avg_buffer.append(dst)
            if len(avg_buffer) == avg_len:
                corners = [[], [], [], []]
                for m in avg_buffer:
                    for i, p in enumerate(m):
                        x, y = p[0][0], p[0][1]
                        corners[i].append((x, y))
                dst = []
                num_outliers = int(avg_len / 4) # on each end
                for p in corners:
                    x_avg = sum(sorted(x for x, y in p)[num_outliers:-num_outliers]) / (avg_len - 2*num_outliers)
                    y_avg = sum(sorted(y for x, y in p)[num_outliers:-num_outliers]) / (avg_len - 2*num_outliers)
                    dst.append([[x_avg, y_avg]])
                print(dst)

            img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

    else:
        print("Not enough matches are found - %d/%d" % (len(matches),MIN_MATCH_COUNT))
        matchesMask = None


    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    img2 = cv2.drawMatches(img1,kp1,img2,kp2,matches,None,**draw_params)

    cv2.imshow('frame',img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # plt.imshow(img2, 'gray'),plt.show()
