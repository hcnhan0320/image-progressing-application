import cv2
import numpy as np

def histogram_equalization(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    # cân bằng biểu đồ trên kênh U
    img_yuv[:, 2:, 0] = cv2.equalizeHist(img_yuv[:, 2:, 0])
    # chuyển đổi hình ảnh YUV trở lại dạng RBG
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    return img