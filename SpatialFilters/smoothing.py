import cv2     # Thư viện OpenCV
import numpy as np   # Thư viện numy để làm việc dữ liệu kiểu mảng
import matplotlib.pyplot as plt # import thư viện matplotlib để vẽ ảnh

def gaussian_blur(img, value):
    blur_img = cv2.GaussianBlur(img, (5,5), value)
    return blur_img

def box_blur(img, value):
    blur_img = cv2.blur(img, (5,5))
    # blur_img = cv2.GaussianBlur(img, ksize=(KERNEL_WIDTH, KERNEL_HEIGHT), sigmaX=SIGMA_X, sigmaY=SIGMA_Y)
    return blur_img

def median_blur(img, value):
    blur_img = cv2.medianBlur(img, value)
    return blur_img

