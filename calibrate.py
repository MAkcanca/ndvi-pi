import numpy as np
import cv2
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Prepare object points based on the real world space
objp = np.zeros((9*6, 3), np.float32)
objp[:,:2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

# Arrays to store object points and image points from all images.
objpoints = []  # 3d points in real world space
imgpoints_l = []  # 2d points in image plane, from left camera
imgpoints_r = []  # 2d points in image plane, from right camera

# Load images
images_left = glob.glob('left/*.jpg')
images_right = glob.glob('right/*.jpg')

for img_left_path, img_right_path in zip(images_left, images_right):
    print(f"Processing {img_left_path} and {img_right_path}")
    img_left = cv2.imread(img_left_path)
    img_right = cv2.imread(img_right_path)
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret_left, corners_left = cv2.findChessboardCorners(gray_left, (9,6), None)
    ret_right, corners_right = cv2.findChessboardCorners(gray_right, (9,6), None)

    if ret_left and ret_right:
        objpoints.append(objp)

        corners2_left = cv2.cornerSubPix(gray_left, corners_left, (11,11), (-1,-1), criteria)
        imgpoints_l.append(corners2_left)

        corners2_right = cv2.cornerSubPix(gray_right, corners_right, (11,11), (-1,-1), criteria)
        imgpoints_r.append(corners2_right)

# calibrate each camera
ret_l, mtx_l, dist_l, rvecs_l, tvecs_l = cv2.calibrateCamera(objpoints, imgpoints_l, gray_left.shape[::-1], None, None)
ret_r, mtx_r, dist_r, rvecs_r, tvecs_r = cv2.calibrateCamera(objpoints, imgpoints_r, gray_right.shape[::-1], None, None)

# stereo calibration
ret_stereo, mtx_l, dist_l, mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints_l, imgpoints_r, mtx_l, dist_l, mtx_r, dist_r, gray_left.shape[::-1])

# stereo Rectification
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(mtx_l, dist_l, mtx_r, dist_r, gray_left.shape[::-1], R, T)

print("Disparity-to-depth mapping matrix (Q):")
print(Q)

np.savez('stereo_calibration.npz', mtx_l=mtx_l, dist_l=dist_l, mtx_r=mtx_r, dist_r=dist_r, R=R, T=T, E=E, F=F, R1=R1, R2=R2, P1=P1, P2=P2, Q=Q)