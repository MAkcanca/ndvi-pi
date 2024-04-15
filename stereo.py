import cv2
import numpy as np

def load_calibration_data(filename='stereo_calibration.npz'):
    data = np.load(filename)
    return {key: data[key] for key in data.files}

def rectify_images(left_img, right_img, calibration_params):
    R1 = calibration_params['R1']
    R2 = calibration_params['R2']
    P1 = calibration_params['P1']
    P2 = calibration_params['P2']
    map1x, map1y = cv2.initUndistortRectifyMap(calibration_params['mtx_l'], calibration_params['dist_l'], R1, P1, left_img.shape[1::-1], cv2.CV_32FC1)
    map2x, map2y = cv2.initUndistortRectifyMap(calibration_params['mtx_r'], calibration_params['dist_r'], R2, P2, right_img.shape[1::-1], cv2.CV_32FC1)
    
    rectified_left = cv2.remap(left_img, map1x, map1y, cv2.INTER_LINEAR)
    rectified_right = cv2.remap(right_img, map2x, map2y, cv2.INTER_LINEAR)
    return rectified_left, rectified_right

def compute_disparity(rectified_left, rectified_right):
    # Stereo block matching algorithm
    stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
    disparity = stereo.compute(rectified_left, rectified_right)
    return disparity

def save_image(image, filename):
    cv2.imwrite(filename, image)
    print(f"Image saved as {filename}")

def main():
    left_img = cv2.imread('left_image.jpg', cv2.IMREAD_GRAYSCALE)
    right_img = cv2.imread('right_image.jpg', cv2.IMREAD_GRAYSCALE)
    
    calibration_params = load_calibration_data('stereo_calibration.npz')
    
    # Rectify images
    rectified_left, rectified_right = rectify_images(left_img, right_img, calibration_params)
    
    save_image(rectified_left, 'rectified_left.png')
    save_image(rectified_right, 'rectified_right.png')

    disparity = compute_disparity(rectified_left, rectified_right)
    
    # Apply color map and save disparity map
    disparity_normalized = cv2.normalize(disparity, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    disparity_colored = cv2.applyColorMap(np.uint8(disparity_normalized), cv2.COLORMAP_JET)
    save_image(disparity_colored, 'colored_disparity.png')
    np.save('disparity.npy', disparity)

if __name__ == '__main__':
    main()
