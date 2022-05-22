import cv2     # Thư viện OpenCV

def canna_edge_detection(img):
    img_gray = cv2.imread(img, 0)
    resize_img = cv2.resize(img_gray, None, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    return resize_img