import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def load_disparity_map(filename='disparity.npy'):
    return np.load(filename)

def generate_3d_point_cloud(disparity, Q):
    # generate 3D points from disparity map and Q matrix
    h, w = disparity.shape
    points_3D = cv2.reprojectImageTo3D(disparity, Q)
    colors = cv2.cvtColor(left_img, cv2.COLOR_BGR2RGB) 
    mask = disparity > disparity.min()  # A mask of valid pixels
    out_points = points_3D[mask]
    out_colors = colors[mask]
    return out_points, out_colors

def visualize_3d_point_cloud(points, colors):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=colors / 255, s=1, marker='.')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D Point Cloud')
    plt.imsave('point_cloud.png', points)

disparity = load_disparity_map('disparity.npy')
calibration = np.load('stereo_calibration.npz')
Q = calibration['Q']

left_img = cv2.imread('left_image.jpg') 

points, colors = generate_3d_point_cloud(disparity, Q)
visualize_3d_point_cloud(points, colors)