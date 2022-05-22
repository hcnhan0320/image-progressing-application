import cv2
import numpy as np

def log_transformation(img):
    # img_2 = np.uint8(np.log(img))
    # img = cv2.threshold(img_2, 2, 225, cv2.THRESH_TOZERO)[1]
    # Apply log transformation method
    c = 255 / np.log(1 + np.max(img))
    log_image = c * (np.log(img + 1))

    # Specify the data type so that
    # float value will be converted to int
    log_image = np.array(log_image, dtype=np.uint8)

    return log_image