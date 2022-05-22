import cv2
import numpy as np

def histogram_equalization(full_path):
    src = cv2.imread(full_path, 0)
    dst = cv2.equalizeHist(src)
    return dst
