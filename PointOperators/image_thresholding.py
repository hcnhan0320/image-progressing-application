import cv2
import numpy as np


def image_thresholding(img, th):
    img_2 = cv2.threshold(img, th, 225, cv2.THRESH_BINARY)[1]
    return img_2
