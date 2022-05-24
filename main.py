from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QAction, QSlider, QMessageBox, QCheckBox
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import cv2
import sys
# import
from PointOperators.reverse_image import reverse_image
from PointOperators.image_thresholding import image_thresholding
from PointOperators.log_transformation import log_transformation
from PointOperators.gamma_correction import gamma_correction
from PointOperators.histogram_equalization import histogram_equalization

from SpatialFilters.smoothing import gaussian_blur, box_blur, median_blur
from SpatialFilters.sharpening import robert_cross_filter, sobel_filter

from EdgeDetection.canna_edge_detection import canna_edge_detection

class MainUI(QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        # load the ui file
        uic.loadUi("mainUI.ui", self)
        # get image path
        self.full_path_img = ''
        self.img = None
        self.oriImg = None
        self.scale_value = 1
        self.gamma_value = None
        self.gauss_value = None

        # crop image
        cropping = False
        x_start, y_start, x_end, y_end = 0, 0, 0, 0
        # init file (1)
        self.open = self.findChild(QAction, "actionOpen")
        self.exit = self.findChild(QAction, "actionExit")
        self.save = self.findChild(QAction, "actionSave")

        self.raw_img_label = self.findChild(QLabel, "imgRaw")
        self.progressed_img_label = self.findChild(QLabel, "imgProgressed")
        self.value_label = self.findChild(QLabel, "value")
        self.value_label.setText("Value: 0")

        # init point operators (2)
        self.reverse = self.findChild(QAction, "actionReverse")
        self.threshold = self.findChild(QAction, "actionThreshold")
        self.log = self.findChild(QAction, "actionLog")
        self.gamma = self.findChild(QAction, "actionGamma")
        self.histogram_equal = self.findChild(QAction, "actionHistogramEqualization")

        # init smoothing image (3)
        self.box_filter = self.findChild(QAction, "actionBoxFilter")
        self.gaussian_filter = self.findChild(QAction, "actionGaussianFilter")
        self.median_filter = self.findChild(QAction, "actionMedianFilter")

        # init sharpening image (4)
        self.robert_cross_filter = self.findChild(QAction, "actionRobertCrossFilter")
        self.sobel_filter = self.findChild(QAction, "actionSobelFilter")

        # init canny edge detection
        self.canny = self.findChild(QAction, "actionCanny")

        # define slider
        self.scaleSlider = self.findChild(QSlider, "scaleSliderHorizontal")
        self.scaleSlider.setValue(10)
        self.scaleSlider.setMaximum(20)
        self.scaleSlider.valueChanged.connect(self.value_changed_scale)
        self.scaleSlider.setTickPosition(QSlider.TicksBelow)

        self.gammaSlider = self.findChild(QSlider, "gammaSliderHorizontal")
        self.gammaSlider.setMaximum(100)
        self.gammaSlider.valueChanged.connect(self.value_changed_gamma)
        self.gammaSlider.setTickPosition(QSlider.TicksBelow)

        self.thresholdSlider = self.findChild(QSlider, "thresholdSliderHorizontal")
        self.thresholdSlider.setMaximum(255)
        self.thresholdSlider.setValue(120)
        self.thresholdSlider.valueChanged.connect(self.value_changed_threshold)
        self.thresholdSlider.setTickPosition(QSlider.TicksBelow)

        self.gaussianSlider = self.findChild(QSlider, "gaussianBlurSliderHorizontal")
        self.gaussianSlider.setMaximum(50)
        self.gaussianSlider.valueChanged.connect(self.value_changed_gaussian_blur)
        self.gaussianSlider.setTickPosition(QSlider.TicksBelow)

        self.maxValueSlider = self.findChild(QSlider, "maxValueSliderHorizontal")
        self.maxValueSlider.setMaximum(255)
        self.maxValueSlider.valueChanged.connect(self.value_changed_canny)
        self.maxValueSlider.setTickPosition(QSlider.TicksBelow)

        self.minValueSlider = self.findChild(QSlider, "minValueSliderHorizontal")
        self.minValueSlider.setMaximum(255)
        self.minValueSlider.valueChanged.connect(self.value_changed_canny)
        self.minValueSlider.setTickPosition(QSlider.TicksBelow)

        # define canny checkbox
        self.canny_checkbox = self.findChild(QCheckBox, "checkBoxCanny")
        self.canny_checkbox.setChecked(True)

        # action file(1)
        self.exit.triggered.connect(lambda: self.alert_message("Exit!"))
        self.open.triggered.connect(self.open_raw_image)
        self.resetButton.clicked.connect(self.reset_image)
        self.save.triggered.connect(self.save_file)

        # action point operators(2)
        self.reverse.triggered.connect(lambda: self.show_progressed_image(reverse_image(self.img), self.scale_value))
        self.threshold.triggered.connect(lambda: self.show_progressed_image(image_thresholding(self.img, 120), self.scale_value))
        self.log.triggered.connect(lambda: self.show_progressed_image(log_transformation(self.img), self.scale_value))
        self.gamma.triggered.connect(lambda: self.show_progressed_image(gamma_correction(self.img, 0.1), self.scale_value))
        self.histogram_equal.triggered.connect(lambda: self.show_progressed_image(histogram_equalization(self.img), self.scale_value))

        # action smoothing image(3)
        self.box_filter.triggered.connect(lambda: self.show_progressed_image(box_blur(self.img, 10), self.scale_value))
        self.gaussian_filter.triggered.connect(lambda: self.show_progressed_image(gaussian_blur(self.img, 0), self.scale_value))
        self.median_filter.triggered.connect(lambda: self.show_progressed_image(median_blur(self.img, 5), self.scale_value))

        # action sharpening image(4)
        self.robert_cross_filter.triggered.connect(lambda: self.show_progressed_image(robert_cross_filter(self.img), self.scale_value))
        self.sobel_filter.triggered.connect(lambda: self.show_progressed_image(sobel_filter(self.img), self.scale_value))

        # action edge detection (5)
        self.canny.triggered.connect(lambda: self.show_progressed_image(canna_edge_detection(self.full_path_img), self.scale_value))

        # show the app
        self.show()

    def browse_image(self):
        self.fname = QFileDialog.getOpenFileName(self, "Open File", "D:\\Image Progressing Application\\img",
                                                 "All File (*);;PNG Files (*.png);; Jpg Files (*.jpg)")
        full_path = self.fname[0].replace('/', '\\\\')
        self.full_path_img = full_path

    def open_raw_image(self):
        self.browse_image()
        # open the image
        self.pixmap = QPixmap(self.fname[0]).scaledToWidth(500)
        # add img to label
        self.raw_img_label.setPixmap(self.pixmap)
        self.img = cv2.imread(self.full_path_img, cv2.IMREAD_UNCHANGED)
        self.oriImg = self.img.copy()
        self.progressed_img_label.clear()
        self.show_progressed_image(self.oriImg, 1)

    def save_file(self):
        self.fname = QFileDialog.getSaveFileName(self, 'Save File', "D:\\Image Progressing Application\\img",
                                                 "All File (*);;PNG Files (*.png);; Jpg Files (*.jpg)")
        full_path = self.fname[0].replace('/', '\\\\')
        if self.fname:
            cv2.imwrite(full_path, self.img)
        else:
            print("error")

    def convert_cv_qt(self, cv_img, scale):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaledToWidth(500*scale)
        return QPixmap.fromImage(p)

    def show_progressed_image(self, progressed_img, scale):
        self.progressed_img_label.clear()
        self.img = progressed_img
        cv_img = self.convert_cv_qt(progressed_img, scale)
        self.progressed_img_label.setPixmap(cv_img)

    def reset_image(self):
        self.show_progressed_image(self.oriImg, 1)
        self.scaleSlider.setValue(10)
        self.value_label.setText("Value: 0")
        self.gamma_value = None
        self.gauss_value = None

    def value_changed_gamma(self, value):
        if self.full_path_img == '':
            self.alert_message("You need to open image first!")
        else:
            if value == 0:
                self.alert_message("Value need to be greater than 0!")
            else:
                self.value_label.setText("Value: " + str(value/10))
                imgEdit = self.oriImg
                if self.gauss_value != None:
                    imgEdit = gaussian_blur(imgEdit, self.gauss_value)
                self.show_progressed_image(gamma_correction(imgEdit, value/10), self.scale_value)
                self.gamma_value = value/10

    def value_changed_threshold(self, value):
        if self.full_path_img == '':
            self.alert_message("You need to open image first!")
        else:
            self.value_label.setText("Value: " + str(value))
            self.show_progressed_image(image_thresholding(self.oriImg, value), self.scale_value)

    def value_changed_gaussian_blur(self, value):
        if self.full_path_img == '':
            self.alert_message("You need to open image first!")
        else:
            self.value_label.setText("Value: " + str(value))
            imgEdit = self.oriImg
            if self.gamma_value != None :
                imgEdit = gamma_correction(imgEdit, self.gamma_value)
            self.show_progressed_image(gaussian_blur(imgEdit, value), self.scale_value)
            self.gauss_value = value

    def value_changed_canny(self, value):
        if self.canny_checkbox.isChecked():
            img_gray = cv2.imread(self.full_path_img, 0)
            self.value_label.setText("Value: " + str(value))
            edges = cv2.Canny(img_gray,self.minValueSlider.value(), self.maxValueSlider.value())
            self.show_progressed_image(edges, self.scale_value)
        else:
            self.alert_message("Canny is unchecked!")
            self.show_progressed_image(self.img, self.scale_value)

    def value_changed_scale(self, value):
        if self.full_path_img == '':
            self.alert_message("You need to open image first!")
        else:
            if value == 0:
                self.alert_message("Value need to be greater than 0!")
            else:
                self.value_label.setText("Value: " + str(value/10))
                resize_img = cv2.resize(self.img, None, fx=self.scaleSlider.value()/10, fy=self.scaleSlider.value()/10, interpolation=cv2.INTER_CUBIC)
                self.show_progressed_image(resize_img, value/10)
                self.scale_value = value/10
                self.img = resize_img

    def alert_message(self, alert_msg):
        msg = QMessageBox()
        msg.setWindowTitle("Alert!")
        msg.setText(alert_msg)
        msg.exec_()

# init
app = QApplication(sys.argv)
UIWindow = MainUI()
app.exec_()