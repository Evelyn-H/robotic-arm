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

mtx = np.array(
[[1.21590122e+03, 0.00000000e+00, 3.75456517e+02],
[0.00000000e+00, 1.17248719e+03, 3.56379910e+02],
[0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
)
dist = np.array([[0.11245815, 0.30009981, 0.0081315, -0.03802704, -0.6149271]])

avg_len = 5
avg_buffer = deque(maxlen=avg_len)

def find_pose(img, corners):
    axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

    # corner points of image
    objp = np.array([
        [0, 0, 0],
        [0, 6, 0],
        [6, 6, 0],
        [6, 0, 0],
    ], dtype=np.float32)
    # Find the rotation and translation vectors.
    _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)

    # project 3D points to image plane
    imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

    def draw(img, corners, imgpts):
        corner = tuple(corners[0].ravel())
        print(imgpts)
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
        return img

    def put_position_orientation_value_to_frame(frame, translation, rotation):
        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(frame,'position(cm)',(10,30), font, 0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,'x:'+str(round(translation[0][0],2)),(250,30), font, 0.7,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'y:'+str(round(translation[1][0],2)),(350,30), font, 0.7,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'z:'+str(round(translation[2][0],2)),(450,30), font, 0.7,(0,0,255),2,cv2.LINE_AA)

        cv2.putText(frame,'orientation(degree)',(10,60), font, 0.7,(0,255,0),1,cv2.LINE_AA)
        cv2.putText(frame,'x:'+str(round(rotation[0][0] * 180. / np.pi,2)),(250,60), font, 0.7,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'y:'+str(round(rotation[1][0] * 180. / np.pi,2)),(350,60), font, 0.7,(0,0,255),2,cv2.LINE_AA)
        cv2.putText(frame,'z:'+str(round(rotation[2][0] * 180. / np.pi,2)),(450,60), font, 0.7,(0,0,255),2,cv2.LINE_AA)

        return frame

    img = draw(img, corners, imgpts)
    img = put_position_orientation_value_to_frame(img, tvecs, rvecs)

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

            dst = np.array(dst, dtype=np.float32)
            frame = cv2.polylines(frame,[np.int32(dst)],True,(255,0,255),3, cv2.LINE_AA)
            # print(repr(dst))
            find_pose(frame, dst)

    else:
        print("Not enough matches are found - %d/%d" % (len(matches), MIN_MATCH_COUNT))
        matchesMask = None


    draw_params = dict(matchColor = (255,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    frame = cv2.drawMatches(img1,kp1,frame,kp2,matches,None,**draw_params)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # plt.imshow(img2, 'gray'),plt.show()
