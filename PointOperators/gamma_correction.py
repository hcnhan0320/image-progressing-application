import cv2
import numpy as np

def gamma_correction(img, c):
    invGamma = 1 / c

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(img, table)
