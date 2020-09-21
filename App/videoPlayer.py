import sys
sys.path.append(".")

from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout
from face_recognizer.detect_faces import face_detection
from datetime import datetime
from PyQt5 import QtCore
from PyQt5 import QtGui
import face_recognition
import pandas as pd
import numpy as np
import imutils
import pickle
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
        self.prototxt = "model/deploy.prototxt.txt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"
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

class FaceRecognizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QtGui.QImage()
        
        self.encodings = "output/encodings2.pickle"
        self.csv = "output/attendance.csv"
        self.prototxt = "model/deploy.prototxt.txt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"

        self.data = pickle.loads(open(self.encodings, "rb").read())
        self.df = pd.read_csv(self.csv, index_col=0)
        self.faceCounter = {name: 0 for name in self.data["names"]}

    def imageDataSlot(self, imageData):
        orig = imageData.copy()
        # imageData = imutils.resize(imageData, width=750)
        rgb = cv2.cvtColor(imageData, cv2.COLOR_BGR2RGB)
        # r = imageData.shape[1] / float(rgb.shape[1])

        (boxes, confidences) = face_detection(image=imageData, prototxt=self.prototxt, model=self.model, min_confidence=0.5)
        boxes = [(box[1], box[2], box[3], box[0]) for (i, box) in enumerate(boxes)]
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over encodings
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                self.data["encodings"], encoding, tolerance=0.5)
            name = "Unknown"
            if True in matches:
                matchIdxs = [i for (i, match) in enumerate(matches) if match]
                counts = {}
                for i in matchIdxs:
                    name = self.data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
                self.faceCounter[name] = self.faceCounter.get(name, 0) + 1
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # resize the bounding boxes
            # top = int(top * r)
            # right = int(right * r)
            # bottom = int(bottom * r)
            # left = int(left * r)

            # draw the predicted face name on the image data
            cv2.rectangle(imageData, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(imageData, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        0.75, (0, 255, 0), 2)

        self.image = self.getQimage(imageData)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def saveDataframe(self):
        self.faceCounter = {key: 1 if value >=30 else 0 for(key, value) in self.faceCounter.items()}
        date_col = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.df[date_col] = self.df["names"].map(lambda name: self.faceCounter[name])
        self.df.to_csv(self.csv)

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