import cv2     # Thư viện OpenCV
import numpy as np   # Thư viện numy để làm việc dữ liệu kiểu mảng
import matplotlib.pyplot as plt # import thư viện matplotlib để vẽ ảnh

# Định nghĩa Robert Cross theo hướng chéo 1
robert_cross_filter1 = np.array(([0, 0, 0],
                              [0,-1, 0],
                              [0, 0, 1]), dtype="float")

# Định nghĩa Robert Cross theo hướng chéo 2
robert_cross_filter2 = np.array(([0, 0, 0],
                              [0, 0,-1],
                              [0, 1, 0]), dtype="float")

def robert_cross_filter(img):
    img_rc_1 = cv2.filter2D(src=img, ddepth=-1, kernel=robert_cross_filter1)
    img_rc_2 = cv2.filter2D(src=img, ddepth=-1, kernel=robert_cross_filter2)
    img_rc_12 = img_rc_1 + img_rc_2
    return img + img_rc_12

# Định nghĩa Sobel theo hướng X
sobel_filter_x = np.array(([-1,-2,-1],
                      [0, 0, 0],
                      [1, 2, 1]), dtype="float")

# Định nghĩa bộ lọc Sobel theo hướng Y
sobel_filter_y = np.array(([-1, 0, 1],
                      [-2, 0, 2],
                      [-1, 0, 1]), dtype="float")

def sobel_filter(img):
    img_sobel_x = cv2.filter2D(src=img, ddepth=-1, kernel=sobel_filter_x)
    img_sobel_y = cv2.filter2D(src=img, ddepth=-1, kernel=sobel_filter_y)
    img_sobel_xy = img_sobel_x + img_sobel_y
    return img + img_sobel_xy