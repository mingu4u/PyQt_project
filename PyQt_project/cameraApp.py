import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
import cv2,imutils
import datetime
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np


from_class = uic.loadUiType("Test9.ui")[0]


class Camera(QThread):
    update = pyqtSignal()
    
    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)

    def stop(self):
        self.running = False

class WindowClass(QMainWindow, from_class) :
    def __init__(self, parnet=None):
        super().__init__()
        
        self.setupUi(self)
        self.setWindowTitle("Hello, Qt!")
        self.Stop.hide()
        self.Start.hide()
        self.shot.hide()
        self.fps = 10
        # self.Frame.setPixmap(self.pixmap)
        # Set up the drawing variables
        self.drawing = False
        self.last_x, self.last_y = None, None

        self.isCameraOn = False
        self.isRecStart = False
        self.redTune = np.full((480,640),self.Rslider.value())
        self.greenTune = np.full((480,640),self.Gslider.value())
        self.blueTune = np.full((480,640),self.Bslider.value())

        # self.tab1.mousePressEvent = self.mousePressEventTab1
        # self.tab1.mouseMoveEvent = self.mouseMoveEventTab1

        self.pixmap = QPixmap()
        self.Frame.setPixmap(self.pixmap)
        self.camera = Camera(self)
        self.camera.daemon = True

        self.record = Camera(self)
        self.record.daemon = True
        self.count = 0
        self.cap = None

        # self.photoFile.clicked.connect(self.openPhoto)
        self.photoFile.clicked.connect(self.openFile_camera)
        self.videoFile.clicked.connect(self.openFile_video)
        self.camera.update.connect(self.updateCamera)
        self.Camonoff.clicked.connect(self.clickCamera)
        self.Start.clicked.connect(self.clickRecord)
        self.Stop.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.shot.clicked.connect(self.capture)
        self.Rslider.valueChanged.connect(self.tuneR)
        self.Gslider.valueChanged.connect(self.tuneG)
        self.Bslider.valueChanged.connect(self.tuneB)
        self.Rcheck.setCheckState(Qt.Checked)
        self.Gcheck.setCheckState(Qt.Checked)
        self.Bcheck.setCheckState(Qt.Checked)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        for kind in ['RGB','HSV']:
            self.colorDetail.addItem(kind)

        for kind in ['Line','rectangle','circle']:
            self.comboBox.addItem(kind)

        self.tuneColor()
        self.colorDetail.currentIndexChanged.connect(self.tuneColor)
        self.colorDetail.setCurrentText(str('RGB'))
        self.tabWidget.setCurrentIndex(0)
        self.comboBox.setCurrentIndex(0)
        # self.comboBox.currentIndexChanged.connect(self.)

    def mousePressEventTab1(self, event):
        if self. currentIndex == 0:
            if event.button() == Qt.LeftButton:
                self.drawing = True
                self.last_x, self.last_y = event.x(), event.y()

    def mouseMoveEventTab1(self, event):
        if self.drawing and self.currentIndex == 0:
            x, y = event.x(), event.y()
            self.drawOnTab1(x, y)
            self.last_x, self.last_y = x, y

    def drawOnTab1(self, x, y):
        painter = QPainter(self.tab1)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, x, y)
        painter.end()

    # def mousePressEventTab1(self, event):
    #     # if self.tabWidget.tabText(self.tabWidget.currentIndex()) == "draw":
    #     #     if self.comboBox.currentText() == "Line":
    #     x = event.x()
    #     y = event.y()
    #     self.drawOnLine(x, y)
    
    def drawOnLine(self, x, y):
        # painter = QPainter(self.tab1)
        # painter.setPen(QPen(Qt.red))
        painter = QPainter(self.Frame.pixmap())
        painter.setPen(QPen(Qt.blue, 10, Qt.SolidLine))
        painter.drawLine(self.x, self.y, x, y)
        painter.end()
        self.update()

        self.x = x
        self.y = y

    # def mouseMoveEvent(self, event):
    #     # if self.tabWidget.currentIndex() == 'draw':
    #     # print('gg')
    #     if self.x is None:
    #         self.x = event.x()
    #         self.y = event.y()
    #         return
        
    #     painter = QPainter(self.Frame.pixmap())
    #     painter.setPen(QPen(Qt.blue, 10, Qt.SolidLine))
    #     painter.drawLine(self.x, self.y, event.x(), event.y())
    #     painter.end()
    #     self.update()

    #     self.x = event.x()
    #     self.y = event.y()
    
    def mouseReleaseEvent(self, event):
        self.x = None
        self.y = None

    def draw(self):
        painter = QPainter(self.Frame.pixmap())
        painter.drawLine(100,100,500,100)
        painter.end

    def openFile_video(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')
        if file:
            self.cap = cv2.VideoCapture(file[0])
            if not self.cap.isOpened():
                return
            self.timer.start(1000//self.fps)

    def update_frame(self):
        if self.cap is not None:
                    # self.isCameraOn = False
                    ret, frame = self.cap.read()
                    if ret:
                        height, width, channel = frame.shape
                        bytes_per_line = 3 * width
                        qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

                        pixmap = QPixmap.fromImage(qt_image)
                        self.Frame.setPixmap(pixmap)
        else:
            self.cap.release()
        # self.isCameraOn = True

        # self.ret, self.frame = cap.read()
        # if self.ret:
        #     self.rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) #프레임에 색입히기
        #     self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
        #                                     QImage.Format_RGB888)

        #     self.pixmap = QPixmap(self.convertToQtFormat)
        #     pixmap = self.pixmap.scaled(self.Frame.width(), self.Frame.height())

        #     self.Frame.setPixmap(pixmap)
        #     self.Frame.update() #프레임 띄우기

        #     time.sleep(0.1)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임
        # else:
        #     breaks

    # cap.release()
    # cv2.destroyAllWindows()

    def openFile_camera(self):
        file = QFileDialog.getOpenFileName(filter='Image (*.*)')
        image = cv2.imread(file[0])
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h,w,c = image.shape
        qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)

        self.pixmap = self.pixmap.fromImage(qimage)
        self.pixmap = self.pixmap.scaled(self.Frame.width(), self.Frame.height())

        self.Frame.setPixmap(self.pixmap)

    def tuneR(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h,w,c = rgb_image.shape
        self.redTune = np.full((h,w),self.Rslider.value())

    def tuneG(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h,w,c = rgb_image.shape
        self.greenTune = np.full((h,w),self.Gslider.value())

    def tuneB(self):
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h,w,c = rgb_image.shape
        self.blueTune = np.full((h,w),self.Bslider.value())

    def capture(self):
        self.now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.now + '.png'
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, image)


    def updateRecording(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(image)

    def clickRecord(self):
        if self.isRecStart == False:
            # self.btnRecord.setText('Rec Stop')
            self.Stop.show()
            self.Start.hide()
            self.isRecStart = True

            self.recordingStart()

        else:
            # self.btnRecord.setText('Rec Start')
            self.Stop.hide()
            self.Start.show()
            self.isRecStart = False

            # self.cameraStop()
            self.recordingStop()

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename, self.fourcc, 20.0, (w, h))


    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()


    def clickCamera(self):
                if self.isCameraOn == False:
                    self.Camonoff.setText('Camera off')
                    self.isCameraOn = True
                    self.Start.show()
                    self.Stop.hide()
                    self.shot.show()
                    self.tuneColor()
                    self.colorDetail.setCurrentText(str('RGB'))

                    self.cameraStart()
                else:
                    self.Camonoff.setText('Camera on')
                    self.isCameraOn = False
                    self.Start.hide()
                    self.Stop.hide()
                    self.shot.hide()

                    self.cameraStop()
                    self.recordingStop()

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)

    def cameraStop(self):
        self.camera.running = False
        self.camera.stop()
        # self.qimage.fill(QColor(0, 0, 0))
        # self.count = 0
        
        self.video.release()


        if self.isRecStart == True:
            self.writer.release()

    def updateCamera(self):
        # self.label.setText('Camera Running : ' + str(self.count))
        # self.count += 1

        retval, image = self.video.read()

        if retval:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            h,w,c = image.shape
            if self.Rcheck.isChecked():
                image[:,:,0] = np.clip(image[:,:,0] + self.redTune, 0, 255)
            if self.Gcheck.isChecked():
                image[:,:,1] = np.clip(image[:,:,1] + self.greenTune, 0, 255)
            if self.Bcheck.isChecked():
                image[:,:,2] = np.clip(image[:,:,2] + self.blueTune, 0, 255)

            self.qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            
            self.image = image
            self.pixmap = self.pixmap.fromImage(self.qimage)
            self.pixmap = self.pixmap.scaled(self.Frame.width(), self.Frame.height())

            self.Frame.setPixmap(self.pixmap)

        # self.count += 1

    def stop(self):
        self.running = False

    def tuneColor(self):
        color_mode = self.colorDetail.currentText()
        if self.isCameraOn == False:
                self.Rcheck.hide()
                self.Gcheck.hide()
                self.Bcheck.hide()
                self.Rslider.hide()
                self.Gslider.hide()
                self.Bslider.hide()
                self.Hue.hide()
                self.Saturation.hide()
                self.Value.hide()
                self.Hslider.hide()
                self.Sslider.hide()
                self.Vslider.hide()

        else:

            if color_mode == 'RGB':
                self.Rcheck.show()
                self.Gcheck.show()
                self.Bcheck.show()
                self.Rslider.show()
                self.Gslider.show()
                self.Bslider.show()
                self.Hue.hide()
                self.Saturation.hide()
                self.Value.hide()
                self.Hslider.hide()
                self.Sslider.hide()
                self.Vslider.hide()
            else:
                self.Rcheck.hide()
                self.Gcheck.hide()
                self.Bcheck.hide()
                self.Rslider.hide()
                self.Gslider.hide()
                self.Bslider.hide()
                self.Hue.show()
                self.Saturation.show()
                self.Value.show()
                self.Hslider.show()
                self.Sslider.show()
                self.Vslider.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
