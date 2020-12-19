import sys
sys.path.append(".")
sys.path.append("./App/utils")

from face_recognizer.recognize_faces_video import FaceRecognizer
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QWidget
from datetime import datetime
import config
import pandas as pd
import numpy as np
import imutils
import pickle
import os

class FaceRecognizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
        
        self.encodings = config.ENCODINGS_PATH
        self.attendance = config.ATTENDANCE_PATH
        self.prototxt = config.PROTOTXT_PATH
        self.model = config.MODEL_PATH

        self.faceRecognizer = FaceRecognizer(self.prototxt, self.model)

        self.data = pickle.loads(open(self.encodings, "rb").read())
        self.df = pd.read_csv(self.attendance, index_col=0)
        self.faceCounter = {name: 0 for name in self.data["names"]}

    def imageDataSlot(self, imageData):
        orig = imageData.copy()
        imageData = imutils.resize(imageData, width=750)
        ratio = imageData.shape[1] / float(imageData.shape[1])
        # ratio = 1

        (boxes, encodings) = self.faceRecognizer.encodeFace(imageData)
        names = self.faceRecognizer.matchFace(encodings, self.data, self.faceCounter)
        frame = self.faceRecognizer.drawFaceBB(imageData, boxes, names, ratio)

        self.image = self.getQimage(imageData)
        if self.image.size() != self.size():
            self.setFixedSize(self.image.size())

        self.update()

    def saveDataframe(self):
        self.faceCounter = {key: 1 if value >=50 else 0 for(key, value) in self.faceCounter.items()}
        date_col = datetime.now().strftime("%A, %b %d, %Y %H:%M")
        self.df[date_col] = self.df["names"].map(lambda name: self.faceCounter[name])
        self.df.to_csv(self.attendance)

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