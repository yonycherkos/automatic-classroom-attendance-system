import sys
sys.path.append(".")
sys.path.append("./App/utils")

from face_recognizer.detect_faces import face_detection
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QWidget
import config
import numpy as np
import cv2
import os

class FaceDetectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
        self.prototxt = config.PROTOTXT_PATH
        self.model = config.MODEL_PATH
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

        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()