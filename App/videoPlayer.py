import sys
sys.path.append(".")

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout
from face_recognizer.detect_faces import face_detection
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np
import cv2
import os


class VideoPlayer(QtCore.QObject):
    imageData = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, camera_port=0, parent=None):
        super().__init__(parent)
        self.camera = cv2.VideoCapture(camera_port)
        self.timer = QtCore.QBasicTimer()

    def startRecording(self):
        self.timer.start(0, self)

    def timerEvent(self, event):
        if (event.timerId() != self.timer.timerId()):
            return

        read, image = self.camera.read()
        if read:
            self.imageData.emit(image)

class FaceDetectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        self.prototxt = "/home/yony/Documents/school_project/final_year_project/automatic-classroom-attendance-system/model/deploy.prototxt.txt"
        self.model = "/home/yony/Documents/school_project/final_year_project/automatic-classroom-attendance-system/model/res10_300x300_ssd_iter_140000.caffemodel"
        self.output = ""
        self.capture = False
        self.total = 0

    def imageDataSlot(self, imageData):
        orig = imageData.copy()
        (boxes, confidences) = face_detection(image=imageData, prototxt=self.prototxt, model=self.model, min_confidence=0.5)
        for ((startX, startY, endX, endY), confidence) in zip(boxes, confidences):
            # draw rectangle around the detected face
            cv2.rectangle(imageData, (startX, startY), (endX, endY), (0, 255, 0), 2)
            text = "{:.2f}".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.putText(imageData, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)

        self.image = self.getQimage(imageData)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())
        
        if self.capture:
            if not os.path.exists(self.output):
                os.makedirs(self.output)
            p = os.path.sep.join([self.output, "{}.png".format(str(self.total).zfill(5))])
            cv2.imwrite(p, orig)
            self.total += 1
            self.capture = False

        self.update()

    def getQimage(self, image: np.ndarray):
        (height, width, colors) = image.shape
        bytesPerLine = 3 * width
        QImage = QtGui.QImage

        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.faceDetectionWidget = FaceDetectionWidget()

        # TODO: set video port
        self.videoPlayer = VideoPlayer()
        self.captureBtn = QPushButton("Capture")
        self.quitBtn = QPushButton("Quit")
        self.videoPlayer.startRecording()

        # Connect the image data signal and slot together
        imageDataSlot = self.faceDetectionWidget.imageDataSlot
        self.videoPlayer.imageData.connect(imageDataSlot)
        # connect the run button to the start recording slot
        self.captureBtn.clicked.connect(self.capture)
        self.quitBtn.clicked.connect(self.quit)

        # Create and set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.faceDetectionWidget)
        layout.addWidget(self.captureBtn)
        layout.addWidget(self.quitBtn)
        self.setLayout(layout)

    def capture(self):
        self.faceDetectionWidget.output = "dataset/yonathan_cherkos_teka"
        self.faceDetectionWidget.capture = True

    def quit(self):
        print("[INFO] {} face captured".format(self.faceDetectionWidget.total))
        cv2.destroyAllWindows()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_widget = MainWidget()
    main_window.setCentralWidget(main_widget)
    main_window.show()
    sys.exit(app.exec_())