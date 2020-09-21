import sys
sys.path.append(".")

from face_recognizer.recognize_faces_video import encodeFace, matchFace, drawFaceBB
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtWidgets import QWidget
from datetime import datetime
import pandas as pd
import numpy as np
import imutils
import pickle
import os

class FaceRecognizerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QImage()
        
        self.encodings = "output/encodings2.pickle"
        self.csv = "output/attendance.csv"
        self.prototxt = "model/deploy.prototxt.txt"
        self.model = "model/res10_300x300_ssd_iter_140000.caffemodel"

        self.data = pickle.loads(open(self.encodings, "rb").read())
        self.df = pd.read_csv(self.csv, index_col=0)
        self.faceCounter = {name: 0 for name in self.data["names"]}

    def imageDataSlot(self, imageData):
        orig = imageData.copy()
        imageData = imutils.resize(imageData, width=750)
        ratio = imageData.shape[1] / float(imageData.shape[1])
        # ratio = 1

        (boxes, encodings) = encodeFace(imageData, self.prototxt, self.model)
        names = matchFace(encodings, self.data, self.faceCounter)
        imageData = drawFaceBB(imageData, boxes, names, ratio)

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

        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)

        image = image.rgbSwapped()
        return image

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()