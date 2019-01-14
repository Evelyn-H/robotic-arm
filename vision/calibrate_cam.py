import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
gridsize = 7
objp = np.zeros((gridsize * gridsize, 3), np.float32)
objp[:, :2] = np.mgrid[0:gridsize, 0:gridsize].T.reshape(-1, 2)
objp = objp * 2

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# images = glob.glob('*.jpg')
cam = cv2.VideoCapture(0)
cam.set(3, 960); cam.set(4, 720)

ret, mtx, dist, rvecs, tvecs = None, None, None, None, None

# mtx = np.array(
#     [[1.21590122e+03, 0.00000000e+00, 3.75456517e+02],
#      [0.00000000e+00, 1.17248719e+03, 3.56379910e+02],
#      [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
# )
# dst = np.array([[0.11245815, 0.30009981, 0.0081315, -0.03802704, -0.6149271]])

#
mtx = np.array(
    [[1.14745099e+03, 0.00000000e+00, 5.18314348e+02],
     [0.00000000e+00, 1.14603781e+03, 3.50345299e+02],
     [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
)
dst = np.array([[3.80986576e-01, -2.77544439e+00, -1.15708998e-03, 1.41828794e-02, 8.76990313e+00]])

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


# for fname in images:
while True:
    # img = cv2.imread(fname)
    _, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if not mtx is None:
        axis = np.float32([[3, 0, 0], [0, 3, 0], [0, 0, -3]]).reshape(-1, 3)

        # img = cv2.imread(fname)
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (gridsize, gridsize),None)

        if ret is True:
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            # Find the rotation and transl(ation vectors.
            _, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)

            def draw(img, corners, imgpts):
                corner = tuple(corners[0].ravel())
                img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
                img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
                img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
                return img

            img = draw(img, corners2, imgpts)
            img = put_position_orientation_value_to_frame(img, tvecs, rvecs)

    cv2.imshow('cam', img)

    k = cv2.waitKey(1) & 0xFF
    if k == ord('i'):
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (gridsize, gridsize), None)

        # If found, add object points, image points (after refining them)
        print(ret)
        if ret is True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (gridsize, gridsize), corners2, ret)
            cv2.imshow('cam', img)
            while not cv2.waitKey(200) & 0xFF == ord('i'):
                pass

    if k == ord('p'):
        # ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        ret, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print(
            ret,
            mtx,
            dist,
            # rvecs,
            # tvecs,
            sep='\n'
        )

        # undistort
        # img = cv2.imread('left12.jpg')
        h, w = img.shape[:2]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))

        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
        # cv2.imwrite('calibresult.png',dst)

        # error
        # tot_error = 0
        # for i in range(len(objpoints)):
        #     imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        #     error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        #     tot_error += error

        # print("total error: ", tot_error/len(objpoints))

        cv2.imshow('cam', img)
        while not cv2.waitKey(200) & 0xFF == ord('p'):
            pass
